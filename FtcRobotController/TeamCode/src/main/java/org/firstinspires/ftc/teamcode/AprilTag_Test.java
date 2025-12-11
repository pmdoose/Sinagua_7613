package org.firstinspires.ftc.teamcode;

import com.qualcomm.robotcore.eventloop.opmode.Autonomous;
import com.qualcomm.robotcore.eventloop.opmode.OpMode;

import org.firstinspires.ftc.teamcode.AprilTag_Cam;
import org.firstinspires.ftc.vision.apriltag.AprilTagDetection;

@Autonomous(name="Camera Test", group="Test")
public class AprilTag_Test extends OpMode {
    AprilTag_Cam tagCam = new AprilTag_Cam();

    @Override
    public void init() {
        tagCam.init(hardwareMap).setTelemetry(telemetry);
    }

    @Override
    public void loop() {
        tagCam.update();
        AprilTagDetection id20 = tagCam.getTagById(20);
        tagCam.displayDetectionTelemetry(id20);
    }

    @Override
    public void stop() {
        tagCam.stop();
    }
}
