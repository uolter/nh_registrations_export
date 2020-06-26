# Notification Hub Export registrations

## Indroduction

This python script can be used to export all registrations from Azure Notification Hub.

It basically uses the standard Azure Rest Api as domented [here](https://docs.microsoft.com/en-us/previous-versions/azure/reference/dn223270%28v%3dazure.100%29).

## Set up

- Create a virtual environment:
```
>> python3 -m venv env
>> source env/bin/activate
```
- Install the dependencies:

```
>> pip install -r requirements.txt
```

## Configurations

- Create the file .env
```
>> touch .env
```

- Add the following configurations

```
SAS_VALUE=<notification hub secret key>
NH_HOSTNAME=<notification hub hostname>
NH_NAME=<notification hub name>
## Optional
OUT_DIR=<directory where registration feeds are saved.>
```

## Run the script

```
>> python main.py
```
