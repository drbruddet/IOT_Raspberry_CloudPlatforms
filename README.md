# IOT_Raspberry_CloudPlatforms

Sending MQTT messages to test cloud infrastructures and IoT Services.

## SAP CLOUD PLATFORM (IoT Neo)
*  TCP_SCP (Use Simple TCP. Raspberry send a TCP message to the SCP Platform)
*  WWS_SCP (Use WebSockets. Raspberry listen the topics. To test, you have to push a message from SCP and ask the raspberry to send you the info you're asking for with the messageID. You can receive CPU infos, CPU Usage, Ram Infos, Disk Space Infos from the Raspberry)
