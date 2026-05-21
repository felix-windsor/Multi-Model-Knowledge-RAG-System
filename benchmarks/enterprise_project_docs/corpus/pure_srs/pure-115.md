# 2001 - elsfork - 3. It should be possible to group both analogue and binary values so they can be read in a

Source: http://nlreqdataset.isti.cnr.it/req.zip

Source file: 2001 - elsfork.pdf

Section: 3. It should be possible to group both analogue and binary values so they can be read in a

3. It should be possible to group both analogue and binary values so they can be read in a
single transaction
5.6 Security
Remote monitoring and operation of devices requires strict security measures for several reasons. To protect the data from being stolen, corrupted, and intentionally falsified, to protect
the device from unauthorised use or to preserve the privacy of monitoring data.
To enforce these security requirements the following functionality is needed: Authentication,
Data Integrity and Data Confidentiality.

5.6.1 Authentication
Server authentication shall ensure the client application that it is truly operating on the intended site. Client authentication ensures that an authorised client/operator is operating the
equipment.
The rights for each user to operate functions and to see data on different levels in the object
hierarchy might be necessary to set. In that way all users can have relevant access to the system and get updated information from the wind power plants.

Page 16

ELFORSK

5.6.2 Data Integrity
Non-corruption of data transferred is necessary, i.e. the ability of a communication system to
deliver data from its originator to its destination with an acceptable residual error rate. This
prevents both malicious and false operation.

5.6.3 Data confidentiality
Data items transferred might need to be encrypted to prevent both malicious and false operation, as well as eavesdropping.
5.7 Performance
The response times of most operational functions and, therefore, of the related communication
does not need to be much faster than one second (human time scale). System management
functions, which shall be available for the operators and control systems, are of low time critical nature. Delay in execution of these functions however should not be more than 2 seconds.
Regarding safety of persons, plant and electric network, the communication system shall not
be of critical nature. No functions regarding safety of persons shall be based on the communication system. No functions regarding safety of plant and electrical network shall be based on
the communication system – all safety functions must be self-contained in the process or in
the devices where systems interface and will trip automatically. In situations where the communication system is completely inaccessible, the plant may be forced to a shutdown by alternative means.

5.7.1 Time Critical Functions
Regarding optimisation of the operation, the communication system has a major role. The
time critical functions include both control and supervision functions. Set points for power
control and Start and Stop commands are the most time critical functions, but also a prompt
response (Acknowledge-on-receive) is important. Periodic on-line operational data is essential for the optimisation of the operation. Finally the operator need to know the status of the
communication system to be able to rely on the presented data.
The time critical functions shall use short messages with a high priority. Data-wise the messages shall be small and shall be transmitted with a minimum of delay. Delays may occur due
to transmission errors, low capacity or low bandwidth of the transport media or network
faults. It is essential for the proper design of the communication system to select methods that
minimise such properties.
Time critical functions must be based on fast and reliable transmission of a number of selected data types. An example of a typical requirement regarding delays for these data is as
follows:
“The overall transfer time for services in time critical functions shall not be more than 0,5
seconds.”

5.7.2 Reliability
Reliability in the sense that data can be retransmitted, reconstructed, or reprocessed if lost or
inaccessible of some reason is essential. Data may be inaccessible e.g. because of faults in the
process (plant), faults in data transport or faults in data processing units. For most data it must
be possible to restore information, including the sequence of events. Local procedures for
recovery may incorporate redundancy of selected functions and backup of data. The communication system shall include functionality to transfer stored data to central storage and processing after restoration of the communication.
Page 17

ELFORSK

To prevent interruptions in the data transfer, the communication system shall allow for redundant communication channels. Processing of data may be carried out simultaneously on more
units. Automatic procedures for detection of communication faults and for managing redundancy of system components shall be established. The physical transport media should possibly be redundant to a certain degree depending on the conditions at the specific plant.
5.8 Compatibility with Existing Systems
There must be a way for existing plants to interface to a new communication system. The
expected solution to interface systems using proprietary methods for communication, e.g.
manufacturer-specified protocols or customer-specified protocols, to new communication
systems is to use gateways.
The interface to existing plants will provide a subset of the functions and data specified in this
Specification. It should however as far as possible be able to present data on the same HMI
and provide as many data as possible for the system databases.

Page 18

ELFORSK
