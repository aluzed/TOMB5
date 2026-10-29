#include "HOSTAUDIO.H"

#include <SDL.h>
#include <LIBSPU.H>

#include <stdio.h>
#include <string.h>

#define SPU_VOICES 24
#define AUDIO_RATE 44100
#define AUDIO_SAMPLES 1024
#define SPU_END_BLOCK 0x07

typedef struct HostVoice
{
	int active;
	unsigned int pos;
	int block_pos;
	int ended;
	int prev1;
	int prev2;
	short block[28];
	short last;
	double phase;
	double step;
	int volume_left;
	int volume_right;
} HostVoice;

static HostVoice voices[SPU_VOICES];
static int last_key_mask;
static SDL_AudioDeviceID audio_device;
static int audio_ready;

static const int filter_pos[5] = { 0, 60, 115, 98, 122 };
static const int filter_neg[5] = { 0, 0, -52, -55, -60 };

static short HostAudio_DecodeNibble(int nibble, int shift, int filter,
                                    int* prev1, int* prev2)
{
	int sample;

	if (nibble & 8)
	{
		nibble -= 16;
	}

	sample = (nibble << 12) >> shift;
	sample += (*prev1 * filter_pos[filter] + *prev2 * filter_neg[filter] + 32) >> 6;

	if (sample > 32767)
	{
		sample = 32767;
	}
	else if (sample < -32768)
	{
		sample = -32768;
	}

	*prev2 = *prev1;
	*prev1 = sample;
	return (short)sample;
}

static void HostAudio_ResetVoice(HostVoice* voice, unsigned short* regs, int index)
{
	unsigned int start = (unsigned int)regs[(index << 3) + 3] << 3;
	unsigned char* ram = Spu_GetRam();
	int ram_size = Spu_GetRamSize();

	memset(voice, 0, sizeof(*voice));

	if (start + 4 <= (unsigned int)ram_size && memcmp(&ram[start], "VAGp", 4) == 0)
	{
		start += 0x30;
	}

	if (start + 16 > (unsigned int)ram_size)
	{
		return;
	}

	voice->active = 1;
	voice->pos = start;
	voice->block_pos = 28;
	voice->phase = 1.0;
	voice->step = (double)(regs[(index << 3) + 2] & 0xFFFF) / 4096.0;
	if (voice->step <= 0.0)
	{
		voice->step = 1.0;
	}
	voice->volume_left = regs[(index << 3)] & 0x7FFF;
	voice->volume_right = regs[(index << 3) + 1] & 0x7FFF;
}

static int HostAudio_NextSample(HostVoice* voice, int index)
{
	unsigned char* ram = Spu_GetRam();
	int ram_size = Spu_GetRamSize();

	while (voice->block_pos >= 28)
	{
		int header;
		int shift;
		int filter;
		int flags;
		int i;

		if (voice->ended || voice->pos + 16 > (unsigned int)ram_size)
		{
			voice->active = 0;
			SpuSetKey(0, 1u << index);
			return 0;
		}

		header = ram[voice->pos];
		shift = header & 0x0F;
		filter = (header >> 4) & 0x0F;
		flags = ram[voice->pos + 1];

		if (shift > 12)
		{
			shift = 12;
		}
		if (filter > 4)
		{
			filter = 4;
		}

		for (i = 0; i < 28; i++)
		{
			int byte = ram[voice->pos + 2 + (i >> 1)];
			int nibble = (i & 1) ? (byte & 0x0F) : ((byte >> 4) & 0x0F);
			voice->block[i] = HostAudio_DecodeNibble(nibble, shift, filter,
			                                         &voice->prev1, &voice->prev2);
		}

		voice->pos += 16;
		voice->block_pos = 0;
		voice->ended = (flags == SPU_END_BLOCK);
	}

	voice->last = voice->block[voice->block_pos++];
	return voice->last;
}

static void HostAudio_Callback(void* userdata, Uint8* stream, int len)
{
	short* out = (short*)stream;
	int frames = len / (int)(sizeof(short) * 2);
	unsigned short* regs = Spu_GetRegisters();
	int key_mask = Spu_GetKeyMask();
	int started = key_mask & ~last_key_mask;
	int stopped = last_key_mask & ~key_mask;
	int i;
	int frame;

	(void)userdata;

	for (i = 0; i < SPU_VOICES; i++)
	{
		if (started & (1 << i))
		{
			HostAudio_ResetVoice(&voices[i], regs, i);
		}
		if (stopped & (1 << i))
		{
			voices[i].active = 0;
		}
	}
	last_key_mask = key_mask;

	for (frame = 0; frame < frames; frame++)
	{
		float left = 0.0f;
		float right = 0.0f;
		int master_left = regs[192] & 0x7FFF;
		int master_right = regs[193] & 0x7FFF;

		for (i = 0; i < SPU_VOICES; i++)
		{
			HostVoice* voice = &voices[i];
			int sample;

			if (!voice->active || !(key_mask & (1 << i)))
			{
				continue;
			}

			if (voice->phase >= 1.0)
			{
				sample = HostAudio_NextSample(voice, i);
				voice->phase -= 1.0;
				while (voice->phase >= 1.0 && voice->active)
				{
					sample = HostAudio_NextSample(voice, i);
					voice->phase -= 1.0;
				}
			}
			else
			{
				sample = voice->last;
			}

			voice->phase += voice->step;

			if (!voice->active)
			{
				continue;
			}

			left += (float)sample * ((float)voice->volume_left / 127.0f) *
			        ((float)master_left / 16383.0f);
			right += (float)sample * ((float)voice->volume_right / 127.0f) *
			         ((float)master_right / 16383.0f);
		}

		if (left > 32767.0f) left = 32767.0f;
		if (left < -32768.0f) left = -32768.0f;
		if (right > 32767.0f) right = 32767.0f;
		if (right < -32768.0f) right = -32768.0f;

		out[frame * 2] = (short)left;
		out[frame * 2 + 1] = (short)right;
	}
}

int HostAudio_Init(void)
{
	SDL_AudioSpec want;
	SDL_AudioSpec have;

	if (audio_ready)
	{
		return 1;
	}

	if (SDL_InitSubSystem(SDL_INIT_AUDIO) != 0)
	{
		printf("[AUDIO] SDL audio unavailable: %s\n", SDL_GetError());
		return 0;
	}

	memset(&want, 0, sizeof(want));
	want.freq = AUDIO_RATE;
	want.format = AUDIO_S16SYS;
	want.channels = 2;
	want.samples = AUDIO_SAMPLES;
	want.callback = HostAudio_Callback;

	audio_device = SDL_OpenAudioDevice(NULL, 0, &want, &have, 0);
	if (audio_device == 0)
	{
		printf("[AUDIO] cannot open audio device: %s\n", SDL_GetError());
		return 0;
	}

	memset(voices, 0, sizeof(voices));
	last_key_mask = Spu_GetKeyMask();
	audio_ready = 1;
	SDL_PauseAudioDevice(audio_device, 0);
	printf("[AUDIO] %d Hz stereo, %d samples\n", have.freq, have.samples);
	return 1;
}

void HostAudio_Shutdown(void)
{
	if (audio_device != 0)
	{
		SDL_CloseAudioDevice(audio_device);
		audio_device = 0;
	}
	audio_ready = 0;
}
