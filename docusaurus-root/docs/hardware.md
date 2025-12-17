---
sidebar_position: 3
title: Hardware Requirements
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Hardware Requirements

This course is technically demanding. It sits at the intersection of three heavy computational loads: **Physics Simulation** (Isaac Sim/Gazebo), **Visual Perception** (SLAM/Computer Vision), and **Generative AI** (LLMs/VLA).

:::warning Heavy Workload
Because the capstone involves a "Simulated Humanoid," the primary investment must be in High-Performance Workstations.
:::

<Tabs>
  <TabItem value="workstation" label="Digital Twin Workstation" default>
    
    ### The "Digital Twin" Workstation (Required per Student)
    This is the most critical component. NVIDIA Isaac Sim requires "RTX" capabilities.
    
    *   **GPU (The Bottleneck)**: NVIDIA RTX 4070 Ti (12GB VRAM) or higher.
        *   *Why*: High VRAM needed for USD assets + VLA models.
        *   *Ideal*: RTX 3090 or 4090 (24GB VRAM).
    *   **CPU**: Intel Core i7 (13th Gen+) or AMD Ryzen 9.
        *   *Why*: Rigid Body Dynamics are CPU-intensive.
    *   **RAM**: 64 GB DDR5.
    *   **OS**: Ubuntu 22.04 LTS (Dual-boot or dedicated).

  </TabItem>
  <TabItem value="edge" label="Physical AI Edge Kit">

    ### The "Physical AI" Edge Kit
    For setting up the nervous system on a desk before deployment.

    *   **The Brain**: NVIDIA Jetson Orin Nano (8GB) or Orin NX (16GB).
    *   **The Eyes**: Intel RealSense D435i or D455 (RGB + Depth).
    *   **The Inner Ear**: Generic USB IMU (BNO055).
    *   **Voice**: USB Microphone/Speaker array (e.g., ReSpeaker).
    
    **Economy Kit (~$700)**:
    *   Jetson Orin Nano Super Dev Kit ($249)
    *   Intel RealSense D435i ($349)
    *   ReSpeaker Mic Array ($69)
    *   SD Card + Wires ($30)

  </TabItem>
  <TabItem value="lab" label="Robot Lab Options">

    ### Option A: The "Proxy" Approach (Budget)
    *   **Robot**: Unitree Go2 Edu (~$1,800 - $3,000).
    *   *Pros*: Durable, ROS 2 support.
    *   *Cons*: Not a biped.

    ### Option B: The "Miniature Humanoid" Approach
    *   **Robot**: Unitree G1 (~$16k) or Robotis OP3 (~$12k).
    *   *Budget Alternative*: Hiwonder TonyPi Pro (~$600) - *Note: Only for kinematics, not AI.*

    ### Option C: The "Premium" Lab
    *   **Robot**: Unitree G1 Humanoid.
    *   *Why*: True dynamic walking + open SDK.

  </TabItem>
</Tabs>

## Cloud vs On-Prem

### Option 2 High OpEx: The "Ether" Lab (Cloud-Native)
*   **Best for**: Rapid deployment, or students with weak laptops.
*   **Instance**: AWS g5.2xlarge (A10G GPU).
*   **Cost**: ~$205 per quarter (120 hours).

:::danger The Latency Trap
Simulating in the cloud works well, but controlling a real robot from a cloud instance is dangerous due to latency.
**Solution**: Train in Cloud -> Download Model -> Flash to Local Jetson.
:::
