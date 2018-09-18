# NV4 Measurement System Architecture Description {#Nv4ArchitectureDoc}

## System View

The delta towards (current) GVP4 implementation is depicted in
separate colors below.

* The FIR camera is connected with a serial link to the ECU with the
Bob in-between in a proper "break-out" configuration: the link is
passed on through the Bob to the ECU (in DC) instead of letting the
ECU mirror video over
the [Bob3 Serial Link Protocol](@ref Bob3Serial). That means that no
extra HiL card is necessary, since the same channel into the ECU can
be used in HiL too.

* The ECU produces video for an in-car Display on yet another serial
  link in "break-out" configuration.
* The serial link(s) for the camera interface are configured via UART
  instead of I2C. The I2C bus for the Display link is for another
  serializer than the ones used in GVP4.
* CAN-FD support was intended for GVP4, but there has been no project
requiring it until now. With CAN-FD support we also want to enable the
two last CAN controllers, which didn't exist in the Bob2.


@startuml
graph system_overview {
  rankdir=LR;

  subgraph cluster_m { #_
    label="Measurement"
    node [shape=plaintext];
    subgraph cluster_ms { #_
      style=filled;
      label="Measurement System";
      Bob -- PC;
    }
    subgraph cluster_sut {
      style=dashed;
      label="System Under Measurement";
      {
        rank=same;
        VehicleNetwork [label="CAN-FD x 6", fontcolor="green"];
        Camera [label="FIR Camera", fontcolor="green"];
        ECU;
      }
      OtherSensors [label="Other Sensors"];
      ECU -- VehicleNetwork;
      OtherSensors -- VehicleNetwork;
    }
  }
  Display [color="green", fontcolor="green"];
  ECU -- Bob -- Camera [color="green"];
  ECU -- Bob -- Display [color="red"];
  ECU -- Bob;
  VehicleNetwork -- Bob;
  PC -- Storage;
}
@enduml

## Configuration

### Streams

The streams to be recorded in the project are defined in
[Measurement System NV4 Stream Specification](@ref Nv4Streams).
These stream settings are configured in a project specific client
product configuration. Bob setup is done
over [RPC](@ref RpcMessagesDoc).


### CAN-FD

The CAN controller configuration shall be part of the
bob_rpc::RequestService::RequestSetCanDriver message. The project
specific settings shall be kept as a client product configuration.

@todo Details filled in when implementing WI-579458.


### FIR Video Link Configuration

The serializer and deserializer break-out on the daughterboard needs
four different configurations:

* DC
* %Replay
* Loop-Back (for self-test use case)
* Camera Only (for camera test use case)

Selecting the configuration is done in the Bob depending on the
current Bob application. The details of the configuration (how to
setup the video driver) is part of the *Nv4DaughterBoard* instance.

@todo How similar to setting up GVP4 DC, replay and loop-back can this
be made?

Simplified data-flows for the use cases are depicted below. Client
recording of video is only required in "DC" and "Camera
Test". Recording of link UART communication is only required in "DC"
and "Replay". The ECU configures the link via UART in both "DC" and
"Replay". In the other two cases the Bob must configure the link.

@startuml
digraph video_channel_config {
  rankdir=LR;
  graph [fontname=Helvetica, fontsize=11];
  node [fontname=Helvetica, fontsize=11];
  edge [fontname=Helvetica, fontsize=10];

  subgraph cluster_legend { #_
    label="Legend";
    color=grey; bgcolor=lightgrey;
    node [style="invisible"];
    datalink1 -> datalink2       [color="black", label="Data"];
    uarteculink1 -> uarteculink2 [color="blue", label="Serializer UART (ECU)"];
    uartcamlink1 -> uartcamlink2 [color="orange", label="Deserializer UART (Camera)"];
    powerlink1 -> powerlink2     [color="green", label="Power"];
  }
  subgraph cluster_dc {
    label="DC";
    {
      rank=same;
      SerializerDC [label="Serializer"];
      DeserializerDC [label="Deserializer"];
    }
    DcBypass [shape=box, label="UART and Data Mirror"];
    SerializerDC -> DeserializerDC [color="green"];
    SerializerDC -> DcBypass       [color="blue"];
    DcBypass -> DcBob              [color="blue"];
    DcBypass -> DeserializerDC     [color="orange"];
    DeserializerDC -> DcBypass     [color="black"];
    DcBypass -> SerializerDC       [color="black"];
    DcBypass -> DcBob              [color="black"];
    DcBob -> DCTool                [color="black"];
    DcBob -> DCTool                [color="blue"];
  }
  subgraph cluster_hil {
    label="Replay";
    {
      rank=same;
      SerializerHiL [label="Serializer"];
      DeserializerHiL [label="Deserializer"];
    }
    HiLBypass [shape=box, label="UART mirror"];
    SerializerHiL -> DeserializerHiL [color="green"];
    SerializerHiL -> HiLBypass       [color="blue"];
    HiLBypass -> ReplayBob           [color="blue"];
    HiLBypass -> DeserializerHiL     [color="orange"];
    ReplayBob -> SerializerHiL       [color="black"];
    ReplayBob -> HiLPlayer           [color="blue"];
    HiLPlayer -> ReplayBob           [color="black"];
  }
  subgraph cluster_test {
    label="Loop-Back";
    {
      rank=same;
      Serializer;
      Deserializer;
    }
    TestBob -> Serializer          [color="green"];
    TestBob -> Deserializer        [color="green"];
    TestBob -> Serializer          [color="blue"];
    TestBob -> Deserializer        [color="orange"];
    TestBob -> Serializer          [color="black"];
    Serializer -> Deserializer     [color="black"];
    Deserializer -> TestBob        [color="black"];
    TestBob -> TestClient          [color="grey", label="Test result"];
  }
  subgraph cluster_camera {
    label="Camera Only";
    {
      rank=top;
      DeserializerCam [label="Deserializer"];
    }
    Bob -> DeserializerCam        [color="green"];
    Bob -> DeserializerCam        [color="orange"];
    DeserializerCam -> Bob        [color="black"];
    Bob -> Client                 [color="black"];
  }
}
@enduml
