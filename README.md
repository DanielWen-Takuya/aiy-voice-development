# aiy-voice-development
Using Google AIY Voice Kit, basic and new function for home use.

# Functionalities : 
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

# Knowing the APIs of AIY Voice: 
- aiy.voicehat (the PCB)
  * get_button() : control the button
    * Synchronous usage : .wait_for_press()
    * Asynchronous usage : register a function on_button_press, then .on_press(on_button_press), once pressed, this function is       called. .on_press(None) to unregister
  * get_led() : control the led
    * .set_state(aiy.voicehat.LED.???) : OFF, ON, BLINK(1s per blink), BLINK_3(3 fast 1 pulse), BEACON(light strong to middle), BEACON_4(ON slowly to OFF and return), BEACON_DARK(OFF), DECAY(ON slowly to OFF), PULSE_SLOW(ON very slowly to OFF and return), PULSE_QUICK(little faster than the slow one)
  * get_status_ui() : return the status of led following the process of voice
    * .set_trigger_sound_wave('sound file') : when "listening", the sound plays out :using 44100Hz and mono file
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

# Psycopg2
- Install postgresql
  * sudo apt-get update
  * sudo apt-get install postgresql postgresql-contrib
  * sudo -u postgres psql
  * ALTER USER postgres WITH PASSWORD 'postgres'： change password
  * Create role : sudo -u postgres createuser --interactive (optional)(in default, role postgres is created)
  * Create database : create database [db name]  
  * Login : psql -U dbuser -d exampledb -h 127.0.0.1 -p 5432
  * Run a file in db: \i pathof_mysqlfile.sql

- Install psycopg2 http://initd.org/psycopg/docs/usage.html
  * pip install psycopg2
  * https://blog.dotmaui.com/2017/08/16/install-psycopg2-for-python-3-via-pip3/
  * import psycopg2
  * connect to an existing database : conn = psycopg2.connect("dbname=test user=postgres password=secret") (surrounded by try-except): change  /etc/postgresql/9.6/main/pg_hba.conf peer->md5
  * Open a cursor to perform operations : cur = conn.cursor()
  * Execute : cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))
  * Update to make change : conn.commit()
  * Query : 
    * cur.execute("SELECT * FROM test;")
    * cur.fetchone()
  * Close communication
    * cur.close()
    * conn.close()
  * Data : 
    * dt = datetime.datetime.now()
    * cur.mogrify("SELECT %s, %s, %s;", (dt, dt.date(), dt.time())) = "SELECT '2010-02-08T01:40:27.425337', '2010-02-08', '01:40:27.425337';"
  * use "with" in cursur
    * conn = psycopg2.connect(DSN)
    * with conn:
        with conn.cursor() as curs:
          curs.execute(SQL1)
    * with conn:
        with conn.cursor() as curs:
          curs.execute(SQL2)
    * conn.close()
  

# Log
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

2018/04/07
- thinking how can the examples helps coding:
  * assistant_library_demo.py : a simple example that controls box by voice beginning by "OK, google"; the backend of detecting hotword and responding are automatically done by simply : 
    *    with Assistant(credentials) as assistant:
    *    for event in assistant.start():dosth()
    * and the process_event() is for the shining of LED by status_ui.status()
    * so a part of functions in Audio Function are done directely by assistent (record and answer), the text needs to be captured and saved by server function(use event.args['text']); play function needs to be done directely by aiy.audio
  * assistant_grpc_demo.py : no using grpc
  * assistant_library_with_button_demo.py : using button to start a conversation in library assistant situation. And the class can be run in background ,use this!
  * assistant_library_with_local_commands_demo.py : can response / add to specific questions, useful in playing songs, recording things...
  * cloudspeech_demo.py : same as assistant, no using

2018/04/08
- tested the led mode
- nearly finish the assistant function (except of playing music, recording sth(try cloud speech))

2018/04/09
- Learning PostgreSQL in Python 3 : Psycopg2

2018/04/11
- set the trigger sound, the volume needs to be small in order not to be loud
- play music by command or button, can be interrupted by pressing button

2018/04/12
- install PostgreSQL

2018/04/13
- create 3 files to create tables, drop tables and insert initial data
- create postgre server to interact with PostgreSQL
- install psycopg2

2018/04/14
- create the tables and insert the data
- check postgre_server.py


# To-Do List
- How can we get the reponse in text ?
- Play a local music using aiy.audio->Done，not using aiy.audio but subprocess
- Set trigger sound->Done
- Record a file in local by command "Record what I am going to say" (file in local - change aiy.assistant, text may be in database)
- Try Postgresql->create all the tables and insertion->test it->Done
- test postgre_server.py->
- play music from the list in db
