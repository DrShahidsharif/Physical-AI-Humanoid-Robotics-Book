---
sidebar_position: 2
title: 'Getting Started with ROS 2'
---

# Getting Started with ROS 2

## Learning Goals

import LearningGoals from '@site/src/components/LearningGoals';

<LearningGoals>
- Install and configure ROS 2 environment
- Understand the workspace structure and build system
- Create your first ROS 2 package
- Run basic ROS 2 commands and tools
</LearningGoals>

## Prerequisites

Before diving into ROS 2, ensure you have:

- A compatible Linux distribution (Ubuntu 22.04 LTS recommended) or Docker container
- Basic knowledge of C++ or Python programming
- Understanding of Linux command line tools
- Familiarity with version control systems (Git)

## Installing ROS 2

The recommended installation method for ROS 2 is via the official packages. We'll use the Humble Hawksbill distribution, which is an LTS version suitable for production robotics applications.

### System Requirements

- 64-bit Ubuntu 22.04 (Jammy Jellyfish)
- At least 4GB RAM
- At least 10GB free disk space
- Internet connection for package installation

## Lab Exercise: ROS 2 Installation and Verification

import LabExercise from '@site/src/components/LabExercise';

<LabExercise title="ROS 2 Installation">
In this lab, you will install ROS 2 Humble Hawksbill on your system and verify the installation by running basic commands.

**Steps**:
1. Set up your locale
2. Add the ROS 2 apt repository
3. Install ROS 2 packages
4. Source the ROS 2 environment
5. Verify installation with basic commands
</LabExercise>

## Summary

This chapter provided the foundation for working with ROS 2. In the next chapter, we'll dive deeper into the core concepts of nodes, topics, and services.