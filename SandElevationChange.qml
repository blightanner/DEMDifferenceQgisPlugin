<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" version="3.22.5-Białowieża" minScale="1e+08" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal fetchMode="0" mode="0" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option value="false" type="bool" name="WMSBackgroundLayer"/>
      <Option value="false" type="bool" name="WMSPublishDataSourceUrl"/>
      <Option value="0" type="int" name="embeddedWidgets/count"/>
      <Option value="Value" type="QString" name="identify/format"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option value="" type="QString" name="name"/>
      <Option name="properties"/>
      <Option value="collection" type="QString" name="type"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling zoomedOutResamplingMethod="nearestNeighbour" enabled="false" zoomedInResamplingMethod="nearestNeighbour" maxOversampling="2"/>
    </provider>
    <rasterrenderer alphaBand="-1" nodataColor="" classificationMin="-2" classificationMax="2" type="singlebandpseudocolor" opacity="0.89" band="1">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader labelPrecision="2" classificationMode="2" maximumValue="2" colorRampType="DISCRETE" clip="1" minimumValue="-2">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option value="215,25,28,3" type="QString" name="color1"/>
              <Option value="43,131,186,255" type="QString" name="color2"/>
              <Option value="0" type="QString" name="discrete"/>
              <Option value="gradient" type="QString" name="rampType"/>
              <Option value="0.0666667;215,25,28,3:0.133333;215,25,28,255:0.2;227,71,49,255:0.266667;238,117,70,255:0.333333;250,163,92,255:0.4;253,193,119,255:0.466667;254,218,148,255:0.533333;255,243,177,255:0.6;242,250,187,255:0.666667;216,239,179,255:0.733333;190,229,170,255:0.8;161,214,166,255:0.866667;122,186,172,255:0.933333;82,159,179,255" type="QString" name="stops"/>
            </Option>
            <prop k="color1" v="215,25,28,3"/>
            <prop k="color2" v="43,131,186,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.0666667;215,25,28,3:0.133333;215,25,28,255:0.2;227,71,49,255:0.266667;238,117,70,255:0.333333;250,163,92,255:0.4;253,193,119,255:0.466667;254,218,148,255:0.533333;255,243,177,255:0.6;242,250,187,255:0.666667;216,239,179,255:0.733333;190,229,170,255:0.8;161,214,166,255:0.866667;122,186,172,255:0.933333;82,159,179,255"/>
          </colorramp>
          <item alpha="3" value="-1.733333333333333" color="#d7191c" label="&lt;= -1.73"/>
          <item alpha="21" value="-1.466666666666667" color="#d7191c" label="-1.73 - -1.47"/>
          <item alpha="255" value="-1.2" color="#d9201f" label="-1.47 - -1.20"/>
          <item alpha="255" value="-0.933333333333333" color="#e55135" label="-1.20 - -0.93"/>
          <item alpha="255" value="-0.666666666666667" color="#f1824c" label="-0.93 - -0.67"/>
          <item alpha="255" value="-0.4" color="#fbae66" label="-0.67 - -0.40"/>
          <item alpha="255" value="-0.133333333333333" color="#fdcc83" label="-0.40 - -0.13"/>
          <item alpha="255" value="0.133333333333333" color="#ffe7a3" label="-0.13 - 0.13"/>
          <item alpha="255" value="0.4" color="#f8f7b7" label="0.13 - 0.40"/>
          <item alpha="255" value="0.666666666666667" color="#e1f3b6" label="0.40 - 0.67"/>
          <item alpha="255" value="0.933333333333333" color="#c5e8ad" label="0.67 - 0.93"/>
          <item alpha="255" value="1.2" color="#a7d9a7" label="0.93 - 1.20"/>
          <item alpha="255" value="1.466666666666667" color="#80beab" label="1.20 - 1.47"/>
          <item alpha="255" value="1.733333333333333" color="#55a1b3" label="1.47 - 1.73"/>
          <item alpha="255" value="inf" color="#2b83ba" label="> 1.73"/>
          <rampLegendSettings useContinuousLegend="1" minimumLabel="" orientation="2" direction="0" maximumLabel="" prefix="" suffix="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option value="" type="QChar" name="decimal_separator"/>
                <Option value="6" type="int" name="decimals"/>
                <Option value="0" type="int" name="rounding_type"/>
                <Option value="false" type="bool" name="show_plus"/>
                <Option value="true" type="bool" name="show_thousand_separator"/>
                <Option value="false" type="bool" name="show_trailing_zeros"/>
                <Option value="" type="QChar" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" gamma="1" contrast="-3"/>
    <huesaturation colorizeRed="255" grayscaleMode="0" saturation="0" colorizeGreen="128" colorizeStrength="100" colorizeBlue="128" colorizeOn="0" invertColors="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
