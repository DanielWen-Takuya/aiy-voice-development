# aiy-voice-development
Using Google AIY Voice Kit, basic and new function for home use.

Functionalities : 
- Part AIY Voice Raspberry
  * React to the button : led changes and "listening" to question
  * Control the Speaker : "answer" the question and play the music
  * Infrared Detection : Detect the human being
  * PostgreSQL Server : Save the detection details, aiy actions and access authentication
  * Communicate with Android Phone : Receive the command and return the information
- Part AIY Android Application
  * Communicate with Raspberry : via WLAN
  * Shows information : action list, action graph, detection details, detection graph
  * Send command : get list of music, play music (store in Raspberry), ask questions, led shining...

Knowing the APIs : 
- aiy.voicehat (the PCB)
  * get_button() : control the button
    * Synchronous usage : .wait_for_press()
    * Asynchronous usage : register a function on_button_press, then .on_press(on_button_press), once pressed, this function is       called. .on_press(None) to unregister
  * get_led() : control the led
    * .set_state(aiy.voicehat.LED.???) : OFF, ON, BLINK, BLINK_3(?), BEACON(?), BEACON_4(?), BEACON_DARK(?), DECAY(change slowly?), PULSE_SLOW, PULSE_QUICK
  * get_status_ui() : return the status of led following the process of voice
    * .set_trigger_sound_wave('sound file') : when "listening", the sound plays out
- aiy.audio
  * get_player() : not using unless changing the default player
  * get_recorder() : not using unless changing the default recorder
  * record_to_wave(filepath, duration) : records an audio
  * play_wave(wave_file) : play the wave file
  * play_audio(audio_data) : play an audio
  * say(words, lang=None, volume=None, pitch=None) : say sth by Google TTS engine
    * word : 'Hello'
    * lang : "en-US", "zh-CN", "zh-HK", "fr-FR", "ja-JP"
    * volume : max 100 min 0
    * pitch : ?
- aiy.cloudspeech
  * get_recognizer()
    * recognize(immediate=False) : recognize the speech into word text, immediate only use in existed hotword list
    * expect_hotword(hotword_list) : enables hotword detection
    * expect_phrase(phrase) : register the phrase is more likely to appear
- aiy.i18n (internationalization)
  * set_locale_dir() : set the directory that contains the language bundles
  * set_language_code() : after setting locale dir, the BCP-47 language code will be set
  * get_language_code() : return the code
- aiy.assistant.grpc
  * get_assistant() : return a recognizer that uses Google Assistant APIs
    * .recognize() : return transcript(text to print) and audio(audio to play_audio by aiy.audio)
- google.assistant.library : Google library for Python
  * class .Assistant : use as a ContextManager
    * with Assistant(credentials, device_model_id) as assistant:
    * .start() need to be called
    * .set_mic_mute(is_muted) : stop for the hotword
    * .start_conversation()/.stop_conversation() : manually start/stop a new conversation
    * the assistant run background and generates a stream of Events
      for event in assistant.start():process_event(event)
    * example in aiy website
  

2018/04/04
- The box is assembled and the image is pluged in the card. Raspberry seems working well. Waiting for the keypad.

2018/04/05
- Reading of the examples : 
  * assistant_library_demo.py : proposes a process helper to define the status of Assistant(micphone) (Ready, Listening, thinking, Finish)
  * assistant_grpc_demo.py : shows how we can control the button, get information from Assistant(micphone)
  * assistant_library_with_button_demo.py : proposes a class that assistant works in background and looping for the activation by the button
  * assistant_library_with_local_commands_demo.py : aiming to specific questions(power_off, reboot, say ip) and response
  * cloudspeech_demo.py : Google CloudSpeech can perform as well as Assistant, so recognizing the text

2018/04/06
- Learning APIs.
- Finish the architecture of the system
- Set the functionalities.
