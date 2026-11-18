# ImGui vendu (overlay de debug)

Ce dossier contient une copie **vendorée** de Dear ImGui, utilisée par
l'overlay de debug du backend Vulkan (bascule `F12`, voir `EMULATOR/DEBUGUI.C`).

- Amont : https://github.com/ocornut/imgui
- Version : `v1.91.5` (tag Git, clone `--depth 1`)
- Licence : MIT, voir `LICENSE.txt` (conservée telle quelle)

Fichiers copiés :

```
imgui.cpp  imgui_draw.cpp  imgui_tables.cpp  imgui_widgets.cpp
imgui.h    imgui_internal.h  imconfig.h
imstb_rectpack.h  imstb_textedit.h  imstb_truetype.h
backends/imgui_impl_sdl2.cpp   backends/imgui_impl_sdl2.h
backends/imgui_impl_vulkan.cpp backends/imgui_impl_vulkan.h
```

Les autres dossiers de l'amont (`examples/`, `docs/`, `misc/`, les autres
backends) ne sont pas nécessaires et ne sont pas versionnés.

Mise à jour : remplacer les fichiers ci-dessus par ceux d'un tag plus
récent, puis recompiler (`build/porting/build64`). Le code du projet ne
dépend que des API listées dans `EMULATOR/DEBUGUI.C` et des en-têtes
`imgui.h` / `imgui_impl_sdl2.h` / `imgui_impl_vulkan.h`.
