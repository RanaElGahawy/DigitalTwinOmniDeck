/************************************************************************
Copyright (c) 2020, Unitree Robotics.Co.Ltd. All rights reserved.
Use of this source code is governed by the MPL-2.0 license, see LICENSE.
************************************************************************/

#include <math.h>
#include <iostream>
#include <unistd.h>
#include <string.h>
#include <sio_client.h>
#include <json.hpp>

// Include your socket.io client library
#include "socket.io-client-cpp/src/sio_client.h"

// #include "src/cpp/udp_comm.h"

using namespace UNITREE_LEGGED_SDK;

using json = nlohmann::json;
sio::client sio_client;


// high cmd
constexpr uint16_t TARGET_PORT = 8082;
constexpr uint16_t LOCAL_PORT = 8081;
constexpr char TARGET_IP[] = "192.168.123.220";   // target IP address


//// low cmd
//constexpr uint16_t TARGET_PORT = 8007;
//constexpr uint16_t LOCAL_PORT = 8082;
//constexpr char TARGET_IP[] = "192.168.123.10";   // target IP address

class Custom
{
public:
    Custom(uint8_t level): safe(LeggedType::Aliengo),
        udp(LOCAL_PORT, TARGET_IP,TARGET_PORT, sizeof(HighCmd), sizeof(HighState))
    {
        udp.InitCmdData(cmd);
        //initialize socket.io client

         sio_client.set_open_listener([this]() { std::cout << "Socket.IO connected." << std::endl; });
        sio_client.set_close_listener([this]() { std::cout << "Socket.IO disconnected." << std::endl; });
        sio_client.set_fail_listener([this]() { std::cout << "Socket.IO failed to connect." << std::endl; });

        sio_client.socket("/unity_cmdvel_namespace")->on("unity_cmdvel_event", [this](sio::event& event) { on_message(event); });
        sio_client.connect("http://192.168.123.220:8000");

    }
    void UDPRecv();
    void UDPSend();
    void RobotControl();

    //###
   

    void on_message(sio::event& event)
    {
        auto msg = event.get_message();
        try
        {
            json j = json::parse(msg->get_string());
            cmd.velocity[0] = j["linear"]["x"].get<float>();
            cmd.velocity[1] = j["linear"]["y"].get<float>();
            cmd.yawSpeed = j["angular"]["z"].get<float>();
            std::cout << "Received command: velocity_x=" << cmd.velocity[0] 
                      << ", velocity_y=" << cmd.velocity[1] 
                      << ", yawSpeed=" << cmd.yawSpeed << std::endl;
        }
        catch (const std::exception& e)
        {
            std::cerr << "Error parsing command: " << e.what() << std::endl;
        }
    }

   
//
    Safety safe;
    UDP udp;
    HighCmd cmd = {0};
    HighState state = {0};
    int motiontime = 0;
    float dt = 0.002;     // 0.001~0.01
};

void Custom::UDPRecv()
{
    udp.Recv();
}

void Custom::UDPSend()
{  
    udp.Send();
}

void Custom::RobotControl() 
{
    udp.GetRecv(state);

    std::cout << "motiontime:\t" << motiontime << " " << state.imu.rpy[2] << "\n";
    std::cout<<"crc "<<state.crc<<std::endl;

    // cmd.velocity[0] = 0.0f;
    // cmd.velocity[1] = 0.0f;
    // cmd.position[0] = 0.0f;
    // cmd.position[1] = 0.0f;
    // cmd.yawSpeed = 0.0f;;

    // cmd.mode = 0;
    // cmd.rpy[0]  = 0;
    // cmd.rpy[1] = 0;
    // cmd.rpy[2] = 0;
    // cmd.gaitType = 0;
    // cmd.dBodyHeight = 0;
    // cmd.dFootRaiseHeight = 0;

    // Set default mode and gait type
    cmd.mode = 2; // Walking mode
    cmd.gaitType = 0; // Trot walking

    std::cout << "Updated command: velocity_x=" << cmd.velocity[0]
              << ", velocity_y=" << cmd.velocity[1]
              << ", yawSpeed=" << cmd.yawSpeed << std::endl;
 
    udp.SetSend(cmd);
}

int main(void) 
{
    std::cout << "Communication level is set to HIGH-level." << std::endl
              << "WARNING: Make sure the robot is standing on the ground." << std::endl
              << "Press Enter to continue..." << std::endl;
    std::cin.ignore();


    Custom custom(HIGHLEVEL);
    InitEnvironment();
    LoopFunc loop_control("control_loop", custom.dt,    boost::bind(&Custom::RobotControl, &custom));
    LoopFunc loop_udpSend("udp_send",     custom.dt, 3, boost::bind(&Custom::UDPSend,      &custom));
    LoopFunc loop_udpRecv("udp_recv",     custom.dt, 3, boost::bind(&Custom::UDPRecv,      &custom));

    loop_udpSend.start();
    loop_udpRecv.start();
    loop_control.start();

    while(1){
        sleep(10);
    };

    return 0; 
}
