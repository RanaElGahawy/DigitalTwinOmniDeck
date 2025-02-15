//Do not edit! This file was generated by Unity-ROS MessageGeneration.
using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using Unity.Robotics.ROSTCPConnector.MessageGeneration;
using RosMessageTypes.Std;

namespace RosMessageTypes.ROS
{
    [Serializable]
    public class PoseWithCovarianceStampedMsg : Message
    {
        public const string k_RosMessageName = "ROS/PoseWithCovarianceStamped";
        public override string RosMessageName => k_RosMessageName;

        //  This expresses an estimated pose with a reference coordinate frame and timestamp
        public HeaderMsg header;
        public PoseWithCovarianceMsg pose;

        public PoseWithCovarianceStampedMsg()
        {
            this.header = new HeaderMsg();
            this.pose = new PoseWithCovarianceMsg();
        }

        public PoseWithCovarianceStampedMsg(HeaderMsg header, PoseWithCovarianceMsg pose)
        {
            this.header = header;
            this.pose = pose;
        }

        public static PoseWithCovarianceStampedMsg Deserialize(MessageDeserializer deserializer) => new PoseWithCovarianceStampedMsg(deserializer);

        private PoseWithCovarianceStampedMsg(MessageDeserializer deserializer)
        {
            this.header = HeaderMsg.Deserialize(deserializer);
            this.pose = PoseWithCovarianceMsg.Deserialize(deserializer);
        }

        public override void SerializeTo(MessageSerializer serializer)
        {
            serializer.Write(this.header);
            serializer.Write(this.pose);
        }

        public override string ToString()
        {
            return "PoseWithCovarianceStampedMsg: " +
            "\nheader: " + header.ToString() +
            "\npose: " + pose.ToString();
        }

#if UNITY_EDITOR
        [UnityEditor.InitializeOnLoadMethod]
#else
        [UnityEngine.RuntimeInitializeOnLoadMethod]
#endif
        public static void Register()
        {
            MessageRegistry.Register(k_RosMessageName, Deserialize);
        }
    }
}
