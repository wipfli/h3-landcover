package com.onthegomap.planetiler.examples;

import com.onthegomap.planetiler.FeatureCollector;
import com.onthegomap.planetiler.FeatureMerge;
import com.onthegomap.planetiler.Planetiler;
import com.onthegomap.planetiler.Profile;
import com.onthegomap.planetiler.VectorTile;
import com.onthegomap.planetiler.geo.GeometryException;
import com.onthegomap.planetiler.config.Arguments;
import com.onthegomap.planetiler.reader.SourceFeature;
import com.onthegomap.planetiler.reader.osm.OsmElement;
import com.onthegomap.planetiler.reader.osm.OsmRelationInfo;
import com.onthegomap.planetiler.util.ZoomFunction;

import java.nio.file.Path;
import java.util.List;
import java.io.File;

public class SwissMap implements Profile {

  @Override
  public void processFeature(SourceFeature sourceFeature, FeatureCollector features) {

    String sourceName = sourceFeature.getSource();
    String kind = sourceName.substring(0, sourceName.length() - 13); // Tree-resolution-9, "-resolution-9" has length 13

    if (sourceName.endsWith("-4")) {
      features.polygon("landcover")
        .setMinZoom(1)
        .setMaxZoom(1)
        .setAttr("kind", kind)
        .setPixelTolerance(0.2);
    }

    if (sourceName.endsWith("-4")) {
      features.polygon("landcover")
        .setMinZoom(2)
        .setMaxZoom(2)
        .setAttr("kind", kind)
        .setPixelTolerance(0.45);
      
    }

    if (sourceName.endsWith("-5")) {
      features.polygon("landcover")
        .setMinZoom(3)
        .setMaxZoom(3)
        .setAttr("kind", kind)
        .setPixelTolerance(0.6);
    }

    if (sourceName.endsWith("-5")) {
      features.polygon("landcover")
        .setMinZoom(4)
        .setMaxZoom(4)
        .setAttr("kind", kind)
        .setPixelTolerance(1.0);
    }

    if (sourceName.endsWith("-6")) {
      features.polygon("landcover")
        .setMinZoom(5)
        .setMaxZoom(5)
        .setAttr("kind", kind)
        .setPixelTolerance(0.8);
    }

    if (sourceName.endsWith("-7")) {
      features.polygon("landcover")
        .setMinZoom(6)
        .setMaxZoom(6)
        .setAttr("kind", kind)
        .setPixelTolerance(0.5);
    }

    if (sourceName.endsWith("-8")) {
      features.polygon("landcover")
        .setMinZoom(7)
        .setMaxZoom(7)
        .setAttr("kind", kind)
        .setPixelTolerance(0.5);
    }

    if (sourceName.endsWith("-9")) {
      features.polygon("landcover")
        .setMinZoom(8)
        .setMaxZoom(8)
        .setAttr("kind", kind)
        .setPixelTolerance(0.6);
    }

    if (sourceName.endsWith("-9")) {
      features.polygon("landcover")
        .setMinZoom(9)
        .setMaxZoom(9)
        .setAttr("kind", kind)
        .setPixelTolerance(0.8);
    }
  }

  @Override
  public List<VectorTile.Feature> postProcessLayerFeatures(String layer, int zoom,
    List<VectorTile.Feature> items) {

    if ("landcover".equals(layer)) {
      try {
        double area = 1.0;
        switch (zoom) {
          case 1:
            area = 4;
            break;
          case 2:
            area = 4;
            break;
          case 3:
            area = 6;
            break;
          case 4:
            area = 10;
            break;
          case 5:
            area = 20;
            break;
          case 6:
            area = 20;
            break;
          case 7:
            area = 20;
            break;
          case 8:
            area = 30;
            break;
          case 9:
            area = 30;
            break;
          default:
            area = 30;
            break;
        }
        return FeatureMerge.mergeNearbyPolygons(items, area, area, 1, 1);
      }
      catch (GeometryException e) {
        return null;
      }
    }

    return null;
  }

  @Override
  public String name() {
    return "H3 Landcover";
  }

  @Override
  public String description() {
    return "H3 Landcover";
  }

  @Override
  public String attribution() {
    return "<a href=\"https://doi.org/10.5281/zenodo.3939038\" target=\"_blank\">&copy; Copernicus</a>";
  }

  public static void main(String[] args) throws Exception {
    run(Arguments.fromArgsOrConfigFile(args));
  }

  static void run(Arguments args) throws Exception {
    
    Planetiler p = Planetiler.create(args)
      .setProfile(new SwissMap())
      .overwriteOutput("mbtiles", Path.of("data", "output.mbtiles"));
    
    File folder = new File("../zips"); // contains files like Bare-Snow-resolution-4.zip
    File[] files = folder.listFiles();
    for (File file : files) {
      if (file.isFile() && file.getName().endsWith(".zip")) {
          String fileNameWithoutSuffix = file.getName().replace(".zip", "");
          System.out.println("adding source " + fileNameWithoutSuffix);
          p.addGeoPackageSource("EPSG:4326", fileNameWithoutSuffix, Path.of("..", "zips", fileNameWithoutSuffix + ".zip"), "");
      }
    }
      
    p.run();
  }
}