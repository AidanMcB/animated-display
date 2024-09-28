### How to run

1. Ensure instillation of Python and Pip
- `sudo apt install python3`
- `sudo apt install python3-pip`
2. Create virtual environment
- `python -m venv venv`
3. Activate virtual environment
- For Linux/Mac:
`source venv/bin/activate`
- For windows:
`env\Scripts\activate`
4. Install requirements
- `pip install -r requirements.txt`
5. Run application
- `python main.py`


### Notes
- If running on a Raspberry Pi, may require additional steps
1. Install `portaudio` to before installing the requirements.text file (specifically for pyaudio)
`sudo apt install portaudio19-dev`