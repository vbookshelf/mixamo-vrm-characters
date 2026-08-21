# Mixamo .vrm Characters

This repo:
- Hosts three Mixamo characters in .vrm format.
- Shows a simple step-by-step workflow to convert a character, that you downloaded from Mixamo, from .fbx format to .vrm format.

Created to support non 3D developers, who want to quickly vibe code three.js projects.

<br>


## Characters available

<br>

<img src="images/image1.png" alt="X Bot" height="300">
<p>X Bot</p>

<br>

<img src="images/image2.png" alt="Y Bot" height="300">
<p>Y Bot</p>

<br>

<img src="images/image3.png" alt="Mousey" height="300">
<p>Claire</p>

<br>

## .fbx to .vrm Conversion Workflow

### Step 1
- Download the character from Mixamo -  FBX Binary(.fbx), T-pose<br>https://www.mixamo.com/
- Rename the file to: character.fbx
- Place the file on your desktop.

<br>

<img src="images/image4.png" alt="Mixamo screenshot" height="300">

<br>

### Step 2
- Download and install Blender<br>
https://www.blender.org/

### Step 3
Install the VRM extension in Blender:<br>
- Edit -> Preferences -> Get Extensions
- Type "VRM" into the search bar<br>
- Click Install

<br>
<img src="images/image5.png" alt="Blender screenshot" height="500">

<br>

### Step 4
- In the top bar click "Scripting". It may be hidden so you will need to slide the other buttons to the left to be able to see it.<br>
- Click "+ New"

<br>
<img src="images/image6.png" alt="Blender screenshot" height="500">

<br>

### Step 5
- Copy the code from the mixamo-to-vrm.py file and paste it into blender.
- Then click the play button to run the code.
- A new file named character.vrm will appear on your desktop.<br>
- You can rename this file.
  
<br>
<img src="images/image7.png" alt="Blender screenshot" height="500">

<br>

The .fbx to .vrm conversion process is now complete.

<br>

## Notes
- A vrm character is simply a virtual robot that exposes an API. You can use Javascript code to move the joints and limbs.
- Mixamo licensing conditions:<br>
https://community.adobe.com/questions-696/mixamo-faq-licensing-royalties-ownership-eula-and-tos-589400

<br>

## References

- Three.js 3D Web Dev Experiments<br>
https://github.com/vbookshelf/Three.js-3D-Web-Dev-Experiments

<br>

