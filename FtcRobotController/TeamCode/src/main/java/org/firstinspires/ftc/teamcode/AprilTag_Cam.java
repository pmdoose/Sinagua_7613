package org.firstinspires.ftc.teamcode;

import android.util.Size;

import androidx.annotation.NonNull;

import com.qualcomm.robotcore.hardware.HardwareMap;

import org.firstinspires.ftc.robotcore.external.Telemetry;
import org.firstinspires.ftc.robotcore.external.hardware.camera.WebcamName;
import org.firstinspires.ftc.robotcore.external.navigation.AngleUnit;
import org.firstinspires.ftc.robotcore.external.navigation.DistanceUnit;
import org.firstinspires.ftc.vision.VisionPortal;
import org.firstinspires.ftc.vision.apriltag.AprilTagDetection;
import org.firstinspires.ftc.vision.apriltag.AprilTagProcessor;

import java.util.*;

public class AprilTag_Cam {
    /// == CAMERA CALIBRATION ==
    /// If you do not manually specify calibration parameters, the SDK will attempt
    /// to load a predefined calibration for your camera.
    private String cam_Name = "Webcam 1";
    private Size cam_resoultion = new Size(640, 480); // Sets Camera Resoultion
    private double[] lensIntrinsics = {665.078057816219, 666.3406112108663, 327.37692391898537, 239.56696393516344};


    /// Declare processing objects
    private AprilTagProcessor aprilTagProcessor = null;
    private VisionPortal visionPortal = null;

    /// List for storing detected tags
    private ArrayList<AprilTagDetection> detectedTags = new ArrayList<>();
    /// Telemetry for display
    private Telemetry telemetry = null;

    /// this is the class constructor, because of the method we use for initilization
    /// it is current not used.
    public AprilTag_Cam() {}

    ///  ensures proper closing of processing objects
    public void stop() {
        if (visionPortal != null)
            visionPortal.close();
    }

    /// Sets up the various systems we will be using to see the AprilTags
    public AprilTag_Cam init(@NonNull HardwareMap hwMap) {
        aprilTagProcessor = new AprilTagProcessor.Builder()
                .setDrawTagID(true)  // Draw tag id over camera image
                .setDrawTagOutline(true) // Draw tag outline
                .setDrawAxes(true) // Draw a small axis (helps see tag orentation through the camera)
                .setDrawCubeProjection(true) // Draws a cube over the AprilTag to show where it is being processed in the image*/
                .setOutputUnits(DistanceUnit.METER, AngleUnit.DEGREES) // Sets the units which are being used
                .setLensIntrinsics( // This sets the camera calibration data
                        lensIntrinsics[0],
                        lensIntrinsics[1],
                        lensIntrinsics[2],
                        lensIntrinsics[3])
                .build(); // This Assembles everything together for proper processing

        VisionPortal.Builder builder = new VisionPortal.Builder(); // Defines a new Builder object
        builder.setCamera(hwMap.get(WebcamName.class, cam_Name)); // Assigns the WebCamera to the builder
        builder.setCameraResolution(cam_resoultion); // Sets the camera resoultion
                                                        // (Must be defined or it will auto choose the highest resoultion which can cause issues
        builder.addProcessor(aprilTagProcessor); // Adds the addembled AprilTag Processor to the builder

        visionPortal = builder.build(); // Assembles the builder

        return this;
    }

    // Sets the Telemetry Display object
    public AprilTag_Cam setTelemetry(@NonNull Telemetry telemetry) {
        this.telemetry = telemetry;
        return this;
    }

    // Updates the AprilTag with the current image data
    public void update() {
        if (aprilTagProcessor == null) {return;}

        detectedTags =  aprilTagProcessor.getDetections();
    }

    // returns the list of all detected tags
    public List<AprilTagDetection> getDetectedTags() {
        return detectedTags;
    }

    // This uses the Telemetry object to display everything we know about the AprilTags
    public void displayDetectionTelemetry(AprilTagDetection detectedId)
    {
        if (this.telemetry == null) {return;}
        if (detectedId == null) {return;}

        if (detectedId.metadata != null) {
            telemetry.addLine(String.format("\n==== (ID %d) %s", detectedId.id, detectedId.metadata.name));
            telemetry.addLine(String.format("XYZ %6.1f %6.1f %6.1f  (cm)", detectedId.ftcPose.x*100, detectedId.ftcPose.y*100, detectedId.ftcPose.z*100));
            telemetry.addLine(String.format("PRY %6.1f %6.1f %6.1f  (deg)", detectedId.ftcPose.pitch, detectedId.ftcPose.roll, detectedId.ftcPose.yaw));
            telemetry.addLine(String.format("RBE %6.1f %6.1f %6.1f  (cm, deg, deg)", detectedId.ftcPose.range*100, detectedId.ftcPose.bearing, detectedId.ftcPose.elevation));
        } else {
            telemetry.addLine(String.format("\n==== (ID %d) Unknown", detectedId.id));
            telemetry.addLine(String.format("Center %6.0f %6.0f   (pixels)", detectedId.center.x, detectedId.center.y));
        }
    }

    public AprilTagDetection getTagById(int id) {
        for (AprilTagDetection detection : detectedTags) {
            if (detection.id == id) {
                return detection;
            }
        }
        return null;
    }
}
