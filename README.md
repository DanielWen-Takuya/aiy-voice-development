# aiy-voice-development
Using Google AIY Voice Kit, basic and new function for home use.

Knowing the APIs : 
- aiy.voicehat (the PCB)
  * get_button() : control the button
    % Synchronous usage : .wait_for_press()
    % Asynchronous usage : register a function on_button_press, then .on_press(on_button_press), once pressed, this function is       called. .on_press(None) to unregister
  * get_led() : control the led
    % .set_state(aiy.voicehat.LED.???) : OFF, ON, BLINK, BLINK_3(?), BEACON(?), BEACON_4(?), BEACON_DARK(?), DECAY(change slowly?), PULSE_SLOW, PULSE_QUICK
  * get_status_ui() : return the status of led following the process of voice
    % .set_trigger_sound_wave('sound file') : when "listening", the sound plays out
- aiy.audio
  * get_player() : not using unless changing the default player
  * get_recorder() : not using unless changing the default recorder
  * record_to_wave(filepath, duration) : records an audio
  * play_wave(wave_file) : play the wave file
  * play_audio(audio_data) : play an audio
  * say(words, lang=None, volume=None, pitch=None) : say sth by Google TTS engine
    % word : 'Hello'
    % lang : "en-US", "zh-CN", "zh-HK", "fr-FR", "ja-JP"
    % volume : max 100 min 0
    % pitch : ?
- aiy.cloudspeech
  * get_recognizer()
    % recognize(immediate=False) : recognize the speech into word text, immediate only use in existed hotword list
    % expect_hotword(hotword_list) : enables hotword detection
    % expect_phrase(phrase) : register the phrase is more likely to appear

2018/04/04
The box is assembled and the image is pluged in the card. Raspberry seems working well. Waiting for the keypad.

2018/04/05
Reading of the examples : 
- assistant_library_demo.py : proposes a process helper to define the status of Assistant(micphone) (Ready, Listening, thinking, Finish)
- assistant_grpc_demo.py : shows how we can control the button, get information from Assistant(micphone)
- assistant_library_with_button_demo.py : proposes a class that assistant works in background and looping for the activation by the button
- assistant_library_with_local_commands_demo.py : aiming to specific questions(power_off, reboot, say ip) and response
- cloudspeech_demo.py : Google CloudSpeech can perform as well as Assistant, so recognizing the text


