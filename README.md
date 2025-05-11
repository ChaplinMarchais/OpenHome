# OpenHome

This application allows for registering custom built IoT devices and managing them remotely.

To utilize the system in a development environment there is a `sample.py` program that will emulate an IoT device utilizing the websocket protocol to communicate with the server.

# Running the Server

To run the sample, make sure you have `python3`, `python3-flask` and `pip` installed.

Move into the OpenHomeServer directory `cd ./OpenHomeServer`. Run `pip install -r requirements.txt` to install the dependencies and then run `flask run`.
The app will be served at [http://localhost:3000/](http://localhost:3000/).

# Running the Sample Emulated Device

Run `cd OpenHomeSDK/src/OpenHome` to move into the client library directory.

Run `pip install -r requirements.txt` to install the required dependencies.

Ensure that you have completed the above section and have the server application running on the local network. Then proceed to use the `Log In` link in the navigation bar to register a new account. Upon completing the authentication the application will display a `device_code` on the home page.

Open the `sample.py` file and set the variable `DEVICE_CODE` to be the code displayed on the home page.

Run `python sample.py` to start the emulator application.

# Using the service

After running the sample emulated device you will see a message `Connected to server` which will indicate that the WS connection has been successfuly established. You may then move to the terminal running the server application from the section above and see the log for the device being connected.

Navigating to the Devices page will allow you to see a list of all the devices associated with your account. The Status column will update when the emulated device is connected or terminated to reflect.