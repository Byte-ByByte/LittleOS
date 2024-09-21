@namespace
class SpriteKind:
    SysIcon = SpriteKind.create()
    $Cursor = SpriteKind.create()
def Fakeload():
    global ConsoleInfo, StartupIcon
    ConsoleInfo = "Loading OS"
    StartupIcon = sprites.create(assets.image("""
            placeholder-x64
            """),
        SpriteKind.SysIcon)
    animation.run_image_animation(StartupIcon,
        assets.animation("""
            startupanim
            """),
        50,
        True)
    StartupIcon.set_position(scene.screen_width() / 2, scene.screen_height() / 2)
    pause(5000)
    sprites.destroy(StartupIcon)
def ReloadCursor(CursorImage: Image, Cursor: Sprite):
    global curx, cury, SysCursor
    curx = SysCursor.x
    cury = SysCursor.y
    sprites.destroy(Cursor)
    SysCursor = sprites.create(CursorImage, SpriteKind.player)
    SysCursor.set_position(curx, cury)
    controller.move_sprite(SysCursor, 100, 100)
    SysCursor.set_stay_in_screen(True)

def on_combos_attach_combo():
    global ConsoleOn
    if ConsoleOn:
        ConsoleOn = False
    else:
        ConsoleOn = True
controller.combos.attach_combo("abudlra+b", on_combos_attach_combo)

def on_combos_attach_combo2():
    pass
controller.combos.attach_combo("aba+b", on_combos_attach_combo2)

def PlayEncodedSound(CSVS: str):
    global CommasFound, index2, SoundType, TempFreqencyA, TempFrequencyB, TempVolA, TempVolB, TempDur, FrequencyA, FrequencyB, VolA, VolB, Duration
    CommasFound = 0
    index2 = 0
    SoundType = parse_float(CSVS.char_at(0))
    TempFreqencyA = ""
    TempFrequencyB = ""
    TempVolA = ""
    TempVolB = ""
    TempDur = ""
    FrequencyA = 0
    FrequencyB = 0
    VolA = 0
    VolB = 0
    Duration = 0
    while True:
        if index2 >= 2:
            if CSVS.char_at(index2) == ",":
                CommasFound += 1
                index2 = index2 + 1
            if CommasFound == 0:
                TempFreqencyA = "" + TempFreqencyA + CSVS.char_at(index2)
            if CommasFound == 1:
                FrequencyA = parse_float(TempFreqencyA)
                TempFrequencyB = "" + TempFrequencyB + CSVS.char_at(index2)
            if CommasFound == 2:
                FrequencyB = parse_float(TempFrequencyB)
                TempVolA = "" + TempVolA + CSVS.char_at(index2)
            if CommasFound == 3:
                VolA = parse_float(TempVolA)
                TempVolB = "" + TempVolB + CSVS.char_at(index2)
            if CSVS.char_at(index2) == "e":
                Duration = parse_float(TempDur)
                break
            if CommasFound == 4:
                VolB = parse_float(TempVolB)
                TempDur = "" + TempDur + CSVS.char_at(index2)
        index2 = index2 + 1
    if False:
        console.log_value("SoundType", SoundType)
        console.log_value("FreqA", FrequencyA)
        console.log_value("FreqB", FrequencyB)
        console.log_value("VolA", VolA)
        console.log_value("VolB", VolB)
        console.log_value("Dur", Duration)
    if SoundType == 0:
        music.play(music.create_sound_effect(WaveShape.SINE,
                FrequencyA,
                FrequencyB,
                VolA,
                VolB,
                Duration,
                SoundExpressionEffect.NONE,
                InterpolationCurve.LINEAR),
            music.PlaybackMode.UNTIL_DONE)
    elif SoundType == 1:
        music.play(music.create_sound_effect(WaveShape.SQUARE,
                FrequencyA,
                FrequencyB,
                VolA,
                VolB,
                Duration,
                SoundExpressionEffect.NONE,
                InterpolationCurve.LINEAR),
            music.PlaybackMode.UNTIL_DONE)
    elif SoundType == 2:
        music.play(music.create_sound_effect(WaveShape.SAWTOOTH,
                FrequencyA,
                FrequencyB,
                VolA,
                VolB,
                Duration,
                SoundExpressionEffect.NONE,
                InterpolationCurve.LINEAR),
            music.PlaybackMode.UNTIL_DONE)
    elif SoundType == 3:
        music.play(music.create_sound_effect(WaveShape.TRIANGLE,
                FrequencyA,
                FrequencyB,
                VolA,
                VolB,
                Duration,
                SoundExpressionEffect.NONE,
                InterpolationCurve.LINEAR),
            music.PlaybackMode.UNTIL_DONE)
    elif SoundType == 4:
        music.play(music.create_sound_effect(WaveShape.NOISE,
                FrequencyA,
                FrequencyB,
                VolA,
                VolB,
                Duration,
                SoundExpressionEffect.NONE,
                InterpolationCurve.LINEAR),
            music.PlaybackMode.UNTIL_DONE)
    else:
        print("Error projecting sound type: invalid SoundType, in PlayEncodedSound")
def ChkRegristry():
    if not (blockSettings.exists("RegristryFinished")):
        blockSettings.write_string("StartupSound",
            "0,1000,1000,255,0,200e0,1500,1500,255,0,200e0,1500,1500,255,0,200e0,1000,1000,255,0,200ep200e3,1000,1000,255,0,200e3,2000,2000,255,0,200ef")
        if False:
            blockSettings.write_number("RegristryFinished", 1)
    elif blockSettings.exists("RegristryFinished") and blockSettings.read_number("RegristryFinished") == 0:
        pass
def PlayEncodedSong(CSVSS: str):
    global index, Sound, IsPad
    index = 0
    Sound = ""
    IsPad = False
    while True:
        if CSVSS.char_at(index) == "e":
            if IsPad:
                pause(parse_float(Sound))
            else:
                Sound = "" + Sound + "e"
                PlayEncodedSound(Sound)
            Sound = ""
            IsPad = False
        elif CSVSS.char_at(index) == "f":
            break
        elif CSVSS.char_at(index) == "p":
            IsPad = True
        else:
            Sound = "" + Sound + CSVSS.char_at(index)
        index += 1
ComputerReady: Sprite = None
Sleep = False
Restart = False
Shutdown = False
PlaceholderAnimShutdown: Sprite = None
lmptext: TextSprite = None
LittleMediaPlayerIcon: Sprite = None
fbapptext: TextSprite = None
appfbinteractive: Sprite = None
Close: Sprite = None
IsAppMenuOpen = False
IsPowerMenuOpen = False
ClosePowerBtn: Sprite = None
SleepModeBtn: Sprite = None
RestartBtn: Sprite = None
ShutDownBtn: Sprite = None
PowerMenu: Sprite = None
IsPad = False
Sound = ""
index = 0
Duration = 0
VolB = 0
VolA = 0
FrequencyB = 0
FrequencyA = 0
TempDur = ""
TempVolB = ""
TempVolA = ""
TempFrequencyB = ""
TempFreqencyA = ""
SoundType = 0
index2 = 0
CommasFound = 0
ConsoleOn = False
cury = 0
curx = 0
StartupIcon: Sprite = None
SysCursor: Sprite = None
ConsoleInfo = ""
Sound2 = ""
ProcessCycles = None
ConsoleInfo = "Started StartStack"
ChkRegristry()
if False:
    Fakeload()
StartupLogo = sprites.create(assets.image("""
        SysStartupLogo
        """),
    SpriteKind.SysIcon)
if blockSettings.exists("StartupSound"):
    PlayEncodedSong(blockSettings.read_string("StartupSound"))
else:
    print("StartupSound does not exist; is RegistryFinished?")
pause(500)
ConsoleText = textsprite.create("")
ConsoleText.set_outline(1, 15)
ConsoleText.set_position(8, 14)
scene.set_background_image(assets.image("""
    background
    """))
sprites.destroy(StartupLogo)
StartIcon = sprites.create(assets.image("""
    StartIcon
    """), SpriteKind.SysIcon)
PowerButton = sprites.create(assets.image("""
        poweroptionsbtn
        """),
    SpriteKind.SysIcon)
StartIcon.set_position(9, 112)
PowerButton.set_position(150, 112)
SysCursor = sprites.create(assets.image("""
    Cursor
    """), SpriteKind.$Cursor)
controller.move_sprite(SysCursor, 100, 100)
SysCursor.set_stay_in_screen(True)
Startup = True

def on_update_interval():
    global curx, cury, ConsoleInfo, ConsoleText, PowerMenu, ShutDownBtn, RestartBtn, SleepModeBtn, ClosePowerBtn, IsPowerMenuOpen, IsAppMenuOpen, Close, appfbinteractive, fbapptext, LittleMediaPlayerIcon, lmptext, PlaceholderAnimShutdown, Shutdown, Restart, Sleep, StartIcon, PowerButton, ComputerReady
    if ConsoleOn:
        ConsoleText.set_text(ConsoleInfo)
    else:
        ConsoleText.set_text("")
    if Startup:
        curx = SysCursor.x
        cury = SysCursor.x
        if controller.A.is_pressed():
            if SysCursor.overlaps_with(PowerButton):
                ConsoleInfo = "PowerMenuOpened"
                color.start_fade(color.original_palette, color.gray_scale, 200)
                sprites.destroy_all_sprites_of_kind(SpriteKind.SysIcon)
                sprites.destroy_all_sprites_of_kind(SpriteKind.text)
                ConsoleText = textsprite.create("")
                ConsoleText.set_outline(1, 15)
                ConsoleText.set_position(8, 14)
                PowerMenu = sprites.create(assets.image("""
                        PowerMenuWindow
                        """),
                    SpriteKind.SysIcon)
                PowerMenu.set_position(scene.screen_width() / 2, scene.screen_height() / 2)
                ShutDownBtn = sprites.create(assets.image("""
                        ShutDownBtn
                        """),
                    SpriteKind.SysIcon)
                RestartBtn = sprites.create(assets.image("""
                    RestartBtn
                    """), SpriteKind.SysIcon)
                SleepModeBtn = sprites.create(assets.image("""
                        SleepModeBtn
                        """),
                    SpriteKind.SysIcon)
                ClosePowerBtn = sprites.create(assets.image("""
                    CloseBtn
                    """), SpriteKind.SysIcon)
                ShutDownBtn.set_position(scene.screen_width() / 2 - 20, scene.screen_height() / 2)
                RestartBtn.set_position(scene.screen_width() / 2, scene.screen_height() / 2)
                SleepModeBtn.set_position(scene.screen_width() / 2 + 20, scene.screen_height() / 2)
                ClosePowerBtn.set_position(scene.screen_width() / 2, scene.screen_height() / 2 + 20)
                IsPowerMenuOpen = True
            if SysCursor.overlaps_with(StartIcon):
                ReloadCursor(assets.image("""
                    Cursor
                    """), SysCursor)
                scene.set_background_image(assets.image("""
                    AppMenuBackground
                    """))
                if not (IsAppMenuOpen):
                    IsAppMenuOpen = True
                    ConsoleInfo = "AppMenuOpened"
                    Close = sprites.create(assets.image("""
                        Close
                        """), SpriteKind.SysIcon)
                    appfbinteractive = sprites.create(assets.image("""
                            app-fb icon
                            """),
                        SpriteKind.SysIcon)
                    fbapptext = textsprite.create("File Browser")
                    LittleMediaPlayerIcon = sprites.create(assets.image("""
                            MediaPlayerIcon
                            """),
                        SpriteKind.player)
                    lmptext = textsprite.create("LittleMedia")
                    fbapptext.set_position(40, 52)
                    Close.set_position(144, 10)
                    appfbinteractive.set_position(14, 37)
                    LittleMediaPlayerIcon.set_position(14, 73)
                    lmptext.set_position(39, 90)
                    StartIcon.y += -1
            else:
                ReloadCursor(assets.image("""
                    Cursor
                    """), SysCursor)
            if IsAppMenuOpen:
                if SysCursor.overlaps_with(Close):
                    ConsoleInfo = "AppClosed"
                    scene.set_background_image(assets.image("""
                        background
                        """))
                    sprites.destroy(Close)
                    sprites.destroy(appfbinteractive)
                    sprites.destroy(fbapptext)
                    sprites.destroy(LittleMediaPlayerIcon)
                    sprites.destroy(lmptext)
                    StartIcon.set_position(9, 112)
                    IsAppMenuOpen = False
                if SysCursor.overlaps_with(appfbinteractive):
                    scene.set_background_image(assets.image("""
                        fbwindow
                        """))
                    sprites.destroy(appfbinteractive)
                    sprites.destroy(fbapptext)
                    sprites.destroy(LittleMediaPlayerIcon)
                    sprites.destroy(lmptext)
                if SysCursor.overlaps_with(LittleMediaPlayerIcon):
                    scene.set_background_image(assets.image("""
                        littlemediawindow
                        """))
                    sprites.destroy(appfbinteractive)
                    sprites.destroy(fbapptext)
                    sprites.destroy(LittleMediaPlayerIcon)
                    sprites.destroy(lmptext)
            if IsPowerMenuOpen:
                if SysCursor.overlaps_with(ShutDownBtn):
                    ConsoleInfo = "Shutting Down System"
                    color.start_fade_from_current(color.original_palette)
                    scene.set_background_image(assets.image("""
                        SysBlue
                        """))
                    sprites.destroy_all_sprites_of_kind(SpriteKind.SysIcon)
                    PlaceholderAnimShutdown = sprites.create(assets.image("""
                        SysError
                        """), SpriteKind.player)
                    animation.run_image_animation(PlaceholderAnimShutdown,
                        assets.animation("""
                            PowerDownAnim
                            """),
                        50,
                        True)
                    Shutdown = True
                if SysCursor.overlaps_with(RestartBtn):
                    ConsoleInfo = "Restarting System"
                    color.start_fade_from_current(color.original_palette)
                    scene.set_background_image(assets.image("""
                        SysBlue
                        """))
                    sprites.destroy_all_sprites_of_kind(SpriteKind.SysIcon)
                    PlaceholderAnimShutdown = sprites.create(assets.image("""
                        SysError
                        """), SpriteKind.player)
                    animation.run_image_animation(PlaceholderAnimShutdown,
                        assets.animation("""
                            PowerDownAnim
                            """),
                        50,
                        True)
                    Restart = True
                if SysCursor.overlaps_with(SleepModeBtn):
                    ConsoleInfo = "System in sleep"
                    Sleep = True
                    sprites.destroy(ShutDownBtn)
                    sprites.destroy(SleepModeBtn)
                    sprites.destroy(RestartBtn)
                    sprites.destroy(PowerMenu)
                    sprites.destroy(ClosePowerBtn)
                    pause(100)
                    color.fade_to_black.start_screen_effect(500)
                    StartIcon = sprites.create(assets.image("""
                        StartIcon
                        """), SpriteKind.SysIcon)
                    PowerButton = sprites.create(assets.image("""
                            poweroptionsbtn
                            """),
                        SpriteKind.SysIcon)
                    StartIcon.set_position(9, 112)
                    PowerButton.set_position(150, 112)
                if SysCursor.overlaps_with(ClosePowerBtn):
                    color.start_fade_from_current(color.original_palette, 100)
                    sprites.destroy(ShutDownBtn)
                    sprites.destroy(SleepModeBtn)
                    sprites.destroy(RestartBtn)
                    sprites.destroy(PowerMenu)
                    sprites.destroy(ClosePowerBtn)
                    StartIcon = sprites.create(assets.image("""
                        StartIcon
                        """), SpriteKind.SysIcon)
                    PowerButton = sprites.create(assets.image("""
                            poweroptionsbtn
                            """),
                        SpriteKind.SysIcon)
                    StartIcon.set_position(9, 112)
                    PowerButton.set_position(150, 112)
        if controller.B.is_pressed():
            ReloadCursor(assets.image("""
                CursorRightClick
                """), SysCursor)
        else:
            ReloadCursor(assets.image("""
                Cursor
                """), SysCursor)
        if controller.A.is_pressed():
            ReloadCursor(assets.image("""
                CursorLeftClick
                """), SysCursor)
        else:
            if not (controller.B.is_pressed()):
                ReloadCursor(assets.image("""
                    Cursor
                    """), SysCursor)
        if Shutdown:
            if Math.percent_chance(1):
                scene.set_background_image(assets.image("""
                    SysBlack
                    """))
                sprites.destroy(PlaceholderAnimShutdown)
                ComputerReady = sprites.create(assets.image("""
                        computerready
                        """),
                    SpriteKind.SysIcon)
        if Restart:
            if Math.percent_chance(1):
                game.reset()
        if Restart:
            if Math.percent_chance(1):
                game.reset()
        if Sleep:
            if controller.A.is_pressed():
                ConsoleInfo = "System awoken"
                color.start_fade_from_current(color.original_palette)
game.on_update_interval(10, on_update_interval)
