## Azure text-to-speech for large text files

Use this project to synthesise speech from long text files.

### Note: you can use free tier subscription (as of June 2022)*

### How to use

install the required library

```shell
pip install azure.cognitiveservices.speech
```

provide input.txt file to files folder

Fill the required script parameters on lines 10 to 12:

```python
# INPUTS
subscriptionKey = ""  # SPEECH SERVICES SUBSCRIPTION KEY
region = "westeurope"  # CHANGE TO THE REGION OF YOUR SERVICE
synthesis_voice = 'cs-CZ-AntoninNeural'  # SYNTHESYS VOICE
```

Run the script


*the text is split into smaller chunks to bypass the free tier size limit (always by newlines for seamless transitions) and the audio is then joined into
resulting output file