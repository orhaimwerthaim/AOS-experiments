package finalproject;

import java.awt.Color;
import java.util.ArrayList;
import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfInt;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;


public class FinalProject {
    public static void main(String[] args) {

    System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    Mat image = Imgcodecs.imread("/home/or/catkin_ws/src/panda_demo/scripts/tic12.jpg");

    Mat binaryImage = preprocess(image);

    List<MatOfPoint> contours = new ArrayList<>();
    Imgproc.findContours(binaryImage, contours,new Mat() ,Imgproc.RETR_CCOMP, Imgproc.CHAIN_APPROX_SIMPLE);
    List<MatOfPoint2f> contoursConvert = new ArrayList<>();

    for(MatOfPoint contour : contours) {
        contoursConvert.add(new MatOfPoint2f(contour.toArray()));
    }

    identifyTicTacToeConfiguration(binaryImage,contoursConvert);

}

    private static Mat preprocess(Mat colorImage) {
//      Imgproc.resize(colorImage, colorImage, new Size(489,0));
        Mat grayImage = new Mat() , binaryImage = new Mat();
        Imgproc.cvtColor(colorImage, grayImage,Imgproc.COLOR_BGR2GRAY);
        binaryImage = grayImage;
        Imgproc.threshold(grayImage, binaryImage, 0, 255, Imgproc.THRESH_BINARY_INV | Imgproc.THRESH_OTSU);
        final Mat kernel = Imgproc.getStructuringElement(Imgproc.MORPH_RECT, new Size(5,5));
        Imgproc.morphologyEx(binaryImage, binaryImage, Imgproc.MORPH_CLOSE, kernel);
        return binaryImage;
    }

    private static MatOfPoint2f getApproxPoly(final MatOfPoint2f contour) {
        MatOfPoint2f polyContour = new MatOfPoint2f();
        final double epsillon = Imgproc.arcLength(contour, true) * 0.02;
        final boolean close = true;
        Imgproc.approxPolyDP(contour, polyContour, epsillon, close);
        return polyContour;
    }

    private static void printContourProperties(final MatOfPoint contour) {
        final double contourArea = Imgproc.contourArea(contour);
        MatOfInt convexHull = new MatOfInt();
        Imgproc.convexHull(contour, convexHull);
 //     final double convexHullArea = Imgproc.contourArea(convexHull);
        Rect boundingRect = Imgproc.boundingRect(contour);
        MatOfPoint2f poly =  getApproxPoly(new 
        MatOfPoint2f(contour.toArray()));
        System.out.println("Contour area : " + contourArea);
        System.out.println("Aespect Ratio : " + 
        boundingRect.width/boundingRect.height);
        System.out.println("Extend: " + contourArea/boundingRect.area());
 //     System.out.println("Solidity : " + contourArea/convexHullArea);
        System.out.println("Poly Size : " + poly.size().area() + ", is convex " + Imgproc.isContourConvex(new MatOfPoint(poly.toArray())));
        System.out.println();
    }

    private static void showContourProperties(final Mat input, final List<MatOfPoint> contours) {
        Mat inputCopy = new Mat();
        for(int i = 0; i < contours.size(); i++) {
            input.copyTo(inputCopy);
            Scalar color = new Scalar(255);
            final int thickness = 3;
            Imgproc.drawContours(inputCopy, contours, i, color,thickness);
            printContourProperties(contours.get(i));
            Imgcodecs.imwrite("C://Users//BadarJahan//Desktop//Test-1-check- "+i+".jpg", inputCopy);
        }
    }

    private static ContourType recognizeContourType(final MatOfPoint2f contour) {
        final double contourArea = Imgproc.contourArea(contour);
        final MatOfPoint2f poly = getApproxPoly(contour);
        ContourType type = ContourType.Unknown;
        if((poly.elemSize() > 7 && poly.elemSize() < 10) && contourArea < 1000) {
             type = ContourType.OType;
        }else if(contourArea > 10000) {
            type = ContourType.XType;
        }
        return type;
    }


    private static void identifyTicTacToeConfiguration(final Mat input, final List<MatOfPoint2f> contours) {

        for(MatOfPoint2f contour: contours) {
            ContourType type = recognizeContourType(contour);

            if(type == ContourType.XType) {
                System.out.print("X");
            }else if(type == ContourType.OType) {
                System.out.print("O");
            }
        }
    }
}
