#include "SFX.H"

#include "SOUND.H"
#include "SPUSOUND.H"
#include "SPECIFIC.H"
#include "CAMERA.H"
#include "LOAD_LEV.H"
#include "MATHS.H"

#include <LIBSPU.H>

long SPU_Play(long sample_index, short volume_left, short volume_right, short pitch, int arg_10)
{
	long channel;

	if (sample_index < 0 || sample_index >= MAX_NUM_SOUND_EFFECTS)
	{
		return -2;
	}

	sva.volume.left = volume_left;
	sva.volume.right = volume_right;
	if (pitch <= 0)
	{
		pitch = 0x1000;
	}
	sva.pitch = pitch;
	sva.addr = LadwSampleAddr[sample_index];

	if (sample_index < LnSamplesLoaded)
	{
		channel = SPU_AllocChannel();
		if (channel >= 0)
		{
			LabSampleType[channel] = arg_10;
			sva.mask = 0x93;
			sva.voice = 1 << channel;
			SpuSetKeyOnWithAttr(&sva);
			return channel;
		}
		else
		{
			return -1;
		}
	}
	else
	{
		return -2;
	}
}

int SPU_UpdateStatus()//915FC, 93640 (F)
{
	int i;
	char status[MAX_SOUND_SLOTS];

	SpuGetAllKeysStatus(&status[0]);

	for (i = 0; i < MAX_SOUND_SLOTS; i++)
	{
		if (status[i] - 1 > 1 && LabSampleType[i] != 0)
		{
			SPU_FreeChannel(i);
		}
	}

	return LnFreeChannels;
}

long SPU_AllocChannel()//915B0, 935F4 (F)
{
	if (LnFreeChannels == 0)
	{
		if (SPU_UpdateStatus() == 0)
		{
			return -1;
		}
	}

	//loc_915DC
	return LabFreeChannel[--LnFreeChannels];
}

void SPU_StopAll()
{
	int channel;

	/* Release every SPU voice and rebuild the free-channel list.  Without
	 * this the emulated key-on state survives a return to the title even
	 * though the game has stopped the corresponding sound slots. */
	SpuSetKey(SPU_OFF, SPU_ALLCH);

	for (channel = 0; channel < MAX_SOUND_SLOTS; channel++)
	{
		LabSampleType[channel] = 0;
	}

	LnFreeChannels = 0;
	for (channel = 0; channel < MAX_SOUND_SLOTS; channel++)
	{
		LabFreeChannel[LnFreeChannels++] = channel;
	}
}

void SPU_FreeChannel(int channel_index)//91668, 936AC (F)
{
	LabSampleType[channel_index] = 0;
	LabFreeChannel[LnFreeChannels++] = channel_index;
}

void S_SoundStopSample(int handle)
{
	if (GtSFXEnabled == 0)
	{
		return;
	}

	if (handle >= 0 && handle < MAX_SOUND_SLOTS && LabSampleType[handle] != 0)
	{
		SpuSetKey(SPU_OFF, 1 << handle);
		SPU_FreeChannel(handle);
	}
}

void S_SetReverbType(int reverb)
{
	if (reverb != CurrentReverb)
	{
		CurrentReverb = reverb;
	}
}

void S_SoundStopAllSamples()
{
	if (GtSFXEnabled == 0)
	{
		return;
	}

	SPU_StopAll();
}

void SOUND_EndScene()
{
	//v0 = sound_active
	if (sound_active != 0)
	{
		//s0 = 0;
		//s2 = sample_infos
		//s1 = &LaSlot[0]

		//loc_91DAC
		for (int i = 0; i < MAX_SOUND_SLOTS; i++)
		{
			//v0 = LaSlot[0].nSampleInfo

			if (LaSlot[i].nSampleInfo >= 0)
			{
				//v0 = sample_infos[LaSlot[0].nSampleInfo].flags
				if ((sample_infos[LaSlot[i].nSampleInfo].flags & 0x3) == 3)
				{
					//a2 = LaSlot[0].nVolume
					//a0 = s0
					if (LaSlot[i].nVolume != 0)
					{
						S_SoundSetPanAndVolume(i, LaSlot[i].nPan, LaSlot[i].nVolume & 0xFFFF, LaSlot[i].distance);
						S_SoundSetPitch(i, LaSlot[i].nPitch);
						LaSlot[i].nVolume = 0;
					}
					else
					{
						//loc_91E08
						S_SoundStopSample(i);
						LaSlot[i].nSampleInfo = -1;
					}
				}
				else
				{
					//loc_91E1C
					if (!S_SoundSampleIsPlaying(i))
					{
						S_SoundStopSample(i);
						LaSlot[i].nSampleInfo = -1;
					}
					else
					{
						//a0 = LaSlot[0].pos.x | LaSlot[0].pos.y |LaSlot[0].pos.z
						//a1 = 
						//a2 = 

						if ((LaSlot[i].pos.x | LaSlot[i].pos.y | LaSlot[i].pos.z) != 0)
						{
							GetPanVolume(&LaSlot[i]);
							S_SoundSetPanAndVolume(i, LaSlot[i].nPan, LaSlot[i].nVolume, LaSlot[i].distance);
						}
						//loc_91E64
					}
				}
			}//loc_91E64
		}
	}//loc_91E74
}

void SOUND_Stop()
{
	UNIMPLEMENTED();
}

int PlaySample(int a0, int volume_left, int volume_right, int a3, int arg_10, int t1, int t2)//914C8(<), 9350C(<)
{
	int volume = volume_left;
	int pitch = t2;
	int pan = (short)a3;
	int left = volume;
	int right = volume;

	/* The historical call boundary passes the pitch where a right volume
	 * would be expected and drops the pan (a3).  Rebuild the stereo pair here
	 * from the real sample index (t1), volume, pitch and signed pan. */
	if (pan > 0)
	{
		left = (volume * (32768 - pan)) >> 15;
	}
	else if (pan < 0)
	{
		right = (volume * (32768 + pan)) >> 15;
	}

	if (pitch <= 0)
	{
		pitch = 0x1000;
	}

	return (int)SPU_Play(t1, (short)left, (short)right, (short)pitch, arg_10);
}

int S_SoundPlaySampleLooped(int a0, int a1, int a2, int a3, int arg_10)
{
	if (GtSFXEnabled)
	{
		return PlaySample(arg_10, a1, a2, a3, 2, a0, a2);
	}
	else
	{
		return -3;
	}
}

int S_SoundSampleIsPlaying(int handle)//916F8(<), 9373C(<)
{
	char status;

	if (GtSFXEnabled == 0)
	{
		return 0;
	}

	status = (char)(SpuGetKeyStatus(1 << handle) -1);

	if (status < 2 || LabSampleType[handle] == 0)
	{
		return LabSampleType[handle];
	}

	SPU_FreeChannel(handle);

	return 0;
}

int S_SoundPlaySample(int a0, int a1, int a2, int a3, int arg_10)//91480(<), ?
{
	if (GtSFXEnabled)
	{
		return PlaySample(arg_10, a1, a2, a3, 1, a0, a2);
	}
	else
	{
		return -3;
	}
}

void S_SoundSetPitch(int handle, int nPitch)
{
	if (handle < 0 || handle >= MAX_SOUND_SLOTS)
	{
		return;
	}

	if (nPitch <= 0)
	{
		nPitch = 0x1000;
	}

	sva.mask = 0x10;
	sva.voice = 1 << handle;
	sva.pitch = (short)nPitch;
	SpuSetVoiceAttr(&sva);
}

int S_SoundSetPanAndVolume(int nhandle, int nPan, int nVolume, int distance)
{
	int volume;
	int left;
	int right;

	(void)distance;

	if (nhandle < 0 || nhandle >= MAX_SOUND_SLOTS)
	{
		return -1;
	}

	volume = nVolume & 0x7FFF;
	if (volume > 127)
	{
		volume >>= 7;
	}
	if (volume > 127)
	{
		volume = 127;
	}

	left = volume;
	right = volume;
	nPan = (short)nPan;
	if (nPan > 0)
	{
		left = (volume * (32768 - nPan)) >> 15;
	}
	else if (nPan < 0)
	{
		right = (volume * (32768 + nPan)) >> 15;
	}

	sva.mask = 0x3;
	sva.voice = 1 << nhandle;
	sva.volume.left = (short)left;
	sva.volume.right = (short)right;
	SpuSetVoiceAttr(&sva);
	return 0;
}

void GetPanVolume(struct SoundSlot* slot)
{
	int dx;
	int dz;

	if (slot == NULL)
	{
		return;
	}

	dx = slot->pos.x - camera.pos.x;
	dz = slot->pos.z - camera.pos.z;
	if (dx != 0 || dz != 0)
	{
		slot->nPan = 16 * CamRot.vy + phd_atan_asm(dz, dx);
	}
	/* nVolume is already attenuated by SoundEffect; do not replace it with
	 * the unattenuated OrigVolume. */
}
