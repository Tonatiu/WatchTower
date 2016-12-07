sysDscr = ["1.3.6.1.2.1.1.1.0"]
sysUpTime = "1.3.6.1.2.1.1.3.0"
udpInDatagrams = "1.3.6.1.2.1.7.1.0"
udpInErrors = "1.3.6.1.2.1.7.3.0"
udpOutDatagrams = "1.3.6.1.2.1.7.4.0"
tcpErrorsRecibed = "1.3.6.1.2.1.6.14.0"
tcpSegmentRecibed = "1.3.6.1.2.1.6.10.0"
tcpOutSegs = "1.3.6.1.2.1.6.11.0"
snmpOutGetResponses  = "1.3.6.1.2.1.11.28.0"
hrProcessorLoad_core_1 = "1.3.6.1.2.1.25.3.3.1.2.196608"
hrProcessorLoad_core_2 = "1.3.6.1.2.1.25.3.3.1.2.196609"
hrStorageUsed_ram = "1.3.6.1.2.1.25.2.3.1.6.1"
hrStorageUsed_root = "1.3.6.1.2.1.25.2.3.1.6.31"



mibObjects = [sysUpTime, udpInDatagrams, udpInErrors, 
udpOutDatagrams, tcpErrorsRecibed, tcpSegmentRecibed, 
tcpOutSegs, snmpOutGetResponses, hrProcessorLoad_core_1, hrProcessorLoad_core_2, 
hrStorageUsed_ram, hrStorageUsed_root]

sleeptime = 2