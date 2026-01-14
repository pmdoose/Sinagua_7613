package org.firstinspires.ftc.teamcode;

import com.qualcomm.robotcore.eventloop.opmode.Autonomous;
import com.qualcomm.robotcore.eventloop.opmode.OpMode;

import org.firstinspires.ftc.teamcode.AprilTag_Cam;
import org.firstinspires.ftc.vision.apriltag.AprilTagDetection;

@Autonomous(name="Camera Test", group="Test")
public class AprilTag_Test extends OpMode { // Uses a standard OpMode (may be slightly diffrent from LinearOpMode)
    AprilTag_Cam tagCam = new AprilTag_Cam(); // Reserves a spot in memory for the AprilTags to be processed

    @Override
    public void init() {
        tagCam.init(hardwareMap) //This sets up the hardware
                .setTelemetry(telemetry); //This is only neeeded if you are displaying telemetry in the AprilTag_cam class
    }

    @Override
    public void loop() {
        tagCam.update(); // Updates the AprilTag information using the current image from the camera
        AprilTagDetection id20 = tagCam.getTagById(20); // Searches for an Tag id (returns null if the tag is not found)
        tagCam.displayDetectionTelemetry(id20); // Displays the information to the screen (needs .setTelemetry() to be set)
    }

    @Override
    public void stop() {
        tagCam.stop(); // Cleans everything up, and closes the camera nicely. It's not needed always needed but highly recomened to use.
    }
}
