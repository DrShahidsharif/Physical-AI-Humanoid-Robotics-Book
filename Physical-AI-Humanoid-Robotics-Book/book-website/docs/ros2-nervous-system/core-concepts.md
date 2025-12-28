---
sidebar_position: 3
title: 'Core Concepts of ROS 2'
---

# Core Concepts of ROS 2

## Learning Goals

import LearningGoals from '@site/src/components/LearningGoals';

<LearningGoals>
- Understand the fundamental building blocks of ROS 2
- Implement nodes, topics, services, and actions
- Learn about message types and communication patterns
- Explore parameter management and lifecycle nodes
</LearningGoals>

## Nodes

In ROS 2, a node is a process that performs computation. Nodes are the fundamental building blocks of a ROS 2 system and are typically organized to perform specific tasks. Each node is written in one of the supported languages (C++, Python, etc.) and communicates with other nodes through topics, services, or actions.

### Creating a Node

To create a node, you need to:
1. Initialize the ROS 2 client library
2. Create a node object
3. Define publishers, subscribers, services, or actions
4. Spin the node to process callbacks
5. Clean up resources when done

## Topics and Messages

Topics provide a way for nodes to exchange data through a publish-subscribe communication pattern. Publishers send messages to a topic, and subscribers receive messages from that topic. This decouples the publisher and subscriber, allowing for flexible system design.

### Message Types

ROS 2 provides several built-in message types and allows for custom message definitions. Common message types include:
- `std_msgs`: Basic data types (integers, floats, strings)
- `geometry_msgs`: Spatial information (points, poses, transforms)
- `sensor_msgs`: Sensor data (images, laser scans, IMU data)
- `nav_msgs`: Navigation-related messages (paths, odometry)

## Lab Exercise: Node Communication

import LabExercise from '@site/src/components/LabExercise';

<LabExercise title="Node Communication">
In this lab, you will create two nodes that communicate through a topic. One node will publish sensor data while the other subscribes and processes it.

**Steps**:
1. Create a custom message type
2. Implement a publisher node
3. Implement a subscriber node
4. Build and run the nodes
5. Monitor the communication using ROS 2 tools
</LabExercise>

import DiagramContainer from '@site/src/components/DiagramContainer';

<DiagramContainer title="Node Communication Pattern">
// This would contain a diagram showing publisher-subscriber pattern
// Placeholder for node communication diagram
</DiagramContainer>

## Services and Actions

While topics provide asynchronous communication, services provide synchronous request-response communication. Actions are used for long-running tasks that may provide feedback during execution.

## Summary

This chapter covered the core concepts of ROS 2 communication patterns. In the next chapter, we'll explore advanced topics including multi-robot systems and real-time considerations.