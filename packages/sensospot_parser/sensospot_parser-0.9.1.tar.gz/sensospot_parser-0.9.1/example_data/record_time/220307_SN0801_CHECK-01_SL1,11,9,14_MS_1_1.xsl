<xsl:stylesheet version="1.0"
 xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exsl="http://exslt.org/common"
 xmlns:msxsl="urn:schemas-microsoft-com:xslt"
 xmlns:user="urn:my-scripts"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">

  <xsl:key name="Tables" match="/*/*" use="local-name(.)" />
  <xsl:template match="/">
    <Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
      xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:x="urn:schemas-microsoft-com:office:excel"
      xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
      xmlns:html="http://www.w3.org/TR/REC-html40">
      <Styles>
        <Style ss:ID="s21">
          <NumberFormat ss:Format="0"/>
        </Style>
      </Styles>


      <xsl:for-each select="ScanJobResult/ExperimentResults/AssayResult">

        <xsl:variable name="array_name" select="./@ID" />
        <xsl:for-each select="*">

          <!-- todo: probably can be done with for-each/select -->
          <xsl:if test="starts-with(local-name(),'Channel')">

            <!-- todo: my be ommit channel if there's just a single channel; maybe make it shorter -->
            <xsl:variable name="channel_name" select="local-name()"/>

            <Worksheet ss:Name="{$array_name}_{$channel_name}">

              <xsl:if test = "not(./SpotResults)" >
                <Table x:FullColumns="1" x:FullRows="1">
                  <Row>
                    <Cell>
                      <Data ss:Type="String">
                        <xsl:value-of select="./Status/@Message"/>
                      </Data>
                    </Cell>
                  </Row>
                </Table>
              </xsl:if>

              <xsl:if test = "./SpotResults" >

                <Table x:FullColumns="1" x:FullRows="1">
                  <Row>
                    <Cell>
                      <Data ss:Type="String">
                        <xsl:text > ID </xsl:text>
                      </Data>
                    </Cell>
					
                    <xsl:for-each select="./SpotResults/Spot[1]/Result">
						<xsl:if test = "./@Type = 'System.Boolean' or ./@Type = 'System.String' or ./@Type = 'System.Int32' or ./@Type = 'System.UInt32' or ./@Type = 'System.Double'">
							<Cell>
								<Data ss:Type="String">
									<xsl:value-of select="./@Label"/>
								</Data>
							</Cell>							
                        </xsl:if>
                    </xsl:for-each>
                  </Row>

                  <xsl:for-each select="./SpotResults/Spot">
                    <Row>
                      <Cell>
                        <Data ss:Type="Number">
                          <xsl:value-of select="./@ID"/>
                        </Data>
                      </Cell>

                      <xsl:for-each select="./Result">								
						  <xsl:if test = "./@Type = 'System.Boolean'" >
							  <Cell>
								<Data ss:Type="Boolean">
								  <xsl:if test = "starts-with(./@Value, 'True')" >1</xsl:if>
								  <xsl:if test = "starts-with(./@Value, 'False')" >0</xsl:if>
								</Data>
							  </Cell>
						  </xsl:if>
						  <xsl:if test = "./@Type = 'System.String'" >
							  <Cell>
								<Data ss:Type="String">
								  <xsl:value-of select="./@Value"/>
								</Data>
							  </Cell>
						  </xsl:if>
						  <xsl:if test = "./@Type = 'System.Int32' or ./@Type = 'System.UInt32' or ./@Type = 'System.Double'" >
							  <Cell>
								<Data ss:Type="Number">
								  <xsl:value-of select="./@Value"/>
								</Data>
							  </Cell>
						  </xsl:if>								
                      </xsl:for-each>
                    </Row>
                  </xsl:for-each>

                </Table>
              </xsl:if>

            </Worksheet>
          </xsl:if>
        </xsl:for-each>

      </xsl:for-each>

    </Workbook>
  </xsl:template>

</xsl:stylesheet>
