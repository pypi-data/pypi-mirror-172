<p align="center"><img width='900' src="https://mars.nasa.gov/system/content_pages/main_images/374_mars2020-PIA21635.jpg"></p>
<h1 align='center'>Marstuff</h1>
<h3 align='center'>API Wrapper for NASA's Mars Rover Photos API</h3>
<p align="center">
  <a href="https://pypi.python.org/pypi/marstuff/"><img src='https://img.shields.io/badge/MADE%20WITH-Python-red?style=for-the-badge'/></a>
  <a href="https://pypi.python.org/pypi/marstuff/"><img src='https://img.shields.io/pypi/pyversions/marstuff?style=for-the-badge'/></a>
  <a href="https://pypi.python.org/pypi/marstuff/"><img src='https://img.shields.io/pypi/status/marstuff?style=for-the-badge'/></a>
  <a href="https://pypi.python.org/pypi/marstuff/"><img src='https://img.shields.io/pypi/l/marstuff?style=for-the-badge'/></a>
  <a href="https://pypi.python.org/pypi/marstuff/"><img src='https://img.shields.io/pypi/v/marstuff?style=for-the-badge'/></a>
</p>


## 📝 Description
This is a **Work-In-Progress** Python API Wrapper for NASA's Mars Rover Photos API
which provides both **Synchronous** and **Asynchronous** support.

## 🔥 Getting Started
- ### ⬇️ Installation
  - Via pip
    ```
    pip install marstuff
    ```
- ### ✨ Getting a NASA Developer Key
  - Goto https://api.nasa.gov/
  - Navigate to `Generate API Key` at the top navbar.
  ![image](https://user-images.githubusercontent.com/90889682/136913433-d1324685-4205-4497-a2c7-0619fb1dd97b.png)
  - Fill in your details, and tap `Signup`
  ![image](https://user-images.githubusercontent.com/90889682/136914064-40e4fbfc-e8f3-46b2-b02e-b270c7cd5c09.png)
  - Copy Your API Key
  ![image](https://user-images.githubusercontent.com/90889682/136915687-fcfdc223-e85e-41f6-bcbb-4781ef1e97bc.png)
- ### ⚡ Quickstart
  - Synchronously getting, Viewing and Saving the `Latest Photo` of NASA's `Curiosity` Rover
    ```py
    from marstuff import Client # Import the Client class
    client = Client("Your API Token") # Make a new Client
    
    # Get the latest Photo
    photo = client.get_latest_photo(client.curiosity)
    # OR
    photo = client.curiosity.get_latest_photo()
    
    # Display the Photo
    photo.show()
    # Save the Photo
    photo.save("Latest photo of Curiosity.png")
    ```
  - Asynchronously getting all the photos taken by the `Rear Hazard Avoidance Camera` of NASA's `Curiosity` Rover on sol `3259`
    ```py
    from marstuff import AsyncClient # Import the AsyncClient class
    from marstuff.objects.camera import CAMERAS # Import the list of all CAMERAS
    import asyncio # Import asyncio
    
    client = AsyncClient("Your API Token") # Make a new Client
    
    # Make a function for running asyncio
    async def get_photos():
        # Get the photo by Curiosity on sol 3259 with the RHAZ camera
        photos = await client.curiosity.get_all_photos_by_sol(3259, CAMERAS.RHAZ)
        # OR
        photos = await client.curiosity.rhaz.get_all_photos_by_sol(3259)
        print(photos)
    
    asyncio.run(get_photos())
    
- #### 🧠 General Need-to-Know Stuff!!
  This API currently provides access to 4 NASA Rovers (`Perseverance`, `Curiosity`, `Opportunity`, and `Spirit`)
  Each rover, takes photos of the surface of mars via different cameras
  
  - The cameras of the `Perseverance` Rover are
  
    Abbreviation | Camera                       
    ------------ | ------------------------------
    EDL_RUCAM|Rover Up-Look Camera
    EDL_RDCAM|Rover Down-Look Camera
    EDL_DDCAM|Descent Stage Down-Look Camera
    EDL_PUCAM1|Parachute Up-Look Camera A
    EDL_PUCAM2|Parachute Up-Look Camera B
    NAVCAM_LEFT|Navigation Camera - Left
    NAVCAM_RIGHT|Navigation Camera - Right
    MCZ_RIGHT|Mast Camera Zoom - Right
    MCZ_LEFT|Mast Camera Zoom - Left
    FRONT_HAZCAM_LEFT_A|Front Hazard Avoidance Camera - Left
    FRONT_HAZCAM_RIGHT_A|Front Hazard Avoidance Camera - Right
    REAR_HAZCAM_LEFT|Rear Hazard Avoidance Camera - Left
    REAR_HAZCAM_RIGHT|Rear Hazard Avoidance Camera - Right
    SKYCAM|MEDA Skycam
    SHERLOC_WATSON|SHERLOC WATSON Camera
    
  - Cameras of other Rovers are
  
    Abbreviation | Camera                         | Curiosity | Opportunity | Spirit
    ------------ | ------------------------------ | --------  | ----------- | ------ |
    FHAZ|Front Hazard Avoidance Camera|✔|✔|✔|
    RHAZ|Rear Hazard Avoidance Camera|✔|✔|✔|
    MAST|Mast Camera| ✔||
    CHEMCAM|Chemistry and Camera Complex  |✔||
    MAHLI|Mars Hand Lens Imager|✔||
    MARDI|Mars Descent Imager|✔||
    NAVCAM|Navigation Camera|✔|✔|✔|
    PANCAM|Panoramic Camera| |✔|✔|
    MINITES|Miniature Thermal Emission Spectrometer (Mini-TES)| |✔|✔|
    
  You can query via `sol` or `earth_date`
  - `sol` means `Martian rotation or day` which can be (0 to `Current Sol of Rover`)
  - `earth_date` is in the format of `YYYY-MM-DD`
