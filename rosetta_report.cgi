#!/usr/local/bin/python
#
# Program: rosetta_report.cgi
#
# Purpose: This cgi supports TR4832, creating an online version of
#   W.K. Silvers "Coat Colors of Mice" book.
#
#   To create a table with the following columns:
#
#   1) Nomenclature of alleles used in W.K. Silvers' book
#
#   2) Their current nomenclature used in MGI
#
#   3) All phenotypic alleles for that gene 
#
#
# Requirements Satisfied by This Program: TR4832


import sys
import string
import cgi

import Configuration
config = Configuration.get_Configuration ('Configuration', 1)

import CGI
import db
import mgi_html

DBSERVER    = config['DBSERVER']
DBNAME      = config['DATABASE']
DBUSER      = config['DBUSER']
DBPASSWORD  = config['DBPASSWORD']

db.set_sqlLogin(DBUSER,DBPASSWORD,DBSERVER,DBNAME)


class rosettaReportClass (CGI.CGI):
###########################################################
# Concept: Container class for methods used to create 
#   a rosettaStone table
# IS:   
# HAS: No parameters
# DOES: Creates the rosetta stone table used in
#   W.K. Silvers book
# Implementation: 

    # Row counter used for gray/white table shading 
    totalRowCount = 0

    def openRosettaPage(self):
    #######################################################
    # Purpose: To create a list strings which contain valid HTML
    #   used to return a page to the user
    # Returns: page (list of strings)
    # Assumes: Nothing
    # Effects: Nothing
    # Throws:  Nothing
    
        # Open page and add HTML page headings
        rosettaPage = [ '<HTML><HEAD>', '<TITLE>%s - ' % config['WKSTITLE'],
            '</TITLE>', '</HEAD><BODY BGCOLOR="#FFFFFF">',
            ]

        # Add banner
        rosettaPage.append (
        '<TABLE WIDTH="100%" BORDER=0 CELLPADDING=2 CELLSPACING=1 >'
            '<TR>'
                '<TD WIDTH="100%" BGCOLOR="#D0E0F0" ALIGN="center" VALIGN="center">'
                '<FONT COLOR="#000000" SIZE=5 FACE="Arial,Helvetica">'
                '<B>Coat Color Genes of the Mouse</B></FONT>'
                '</TD>'
            '</TR>'
        '</TABLE>')

        # Add descriptive text
        rosettaPage.append (
            '<H3>Adapted from '
            '<B><I>The Coat Colors of Mice</I></B> by Willys K. Silvers</H3>'
            '<P>The table lists those genes described in The Coat Colors of '
            'Mice (as of 1979), with their current nomenclature and links '
            'to a complete list of alleles for each of these genes. </P>'
            '<P>Please see also a <A HREF="'+ config['COATANOM'] + '" TARGET="_BLANK">table</A> '
            'of all currently known genes in MGI annotated with the phenotype '
            'term "coat color anomalies."</P>'
            )
        
        return rosettaPage
        

    def makeRosettaTable(self,rosettaPage):
    #######################################################
    # Purpose: Add the rosetta data table to the return page.
    #   This method will add a data row for each entry in 
    #   wks_rosetta
    # Returns: rosettaPage (list of strings)
    # Assumes: rosettaPage has already been opened and prepared with
    #   the required HTML tags
    # Effects: rosettaPage
    # Throws:  Nothing
        # Define string literal used to append each data row to table
        # Inputs:
        # 1) Shading
        # 2) URL: To WKS chapter referencing the given gene
        # 3) WKS Gene 
        # 4) URL: To MGI gene detail for given gene
        # 5) MGI gene
        # 6) URL: To MGI allele_report using given 
        # 7) MGI Gene
        
        tableRow = '<TR BGCOLOR=%s>'\
            ' <TD><A HREF = %s>%s</A></TD>'\
            ' <TD><A HREF = %s TARGET="_BLANK">%s</A></TD>'\
            ' <TD><A HREF = %s TARGET="_BLANK">%s</A></TD>'\
            '</TR>'
            
            
        # Pull needed data from database
        # Query 1: Pulls gene data that is in both WK SIlvers book and MGI
        # Query 2: Pulls gene data that is only in the WK SIlvers book
        resultsList = db.sql ([ 
            '''select distinct
            r.wks_markersymbol, r.wks_markerurl,
            r._marker_key, m.symbol, m.name, a.accid
            from wks_rosetta r, mrk_marker m, acc_accession a
            where r._marker_key = m._marker_key
            and   r.wks_markersymbol is not null
            and   r._marker_key = a._object_key
            and   a._logicaldb_key = 1
            and   a.preferred = 1
            and   a._mgitype_key = 2            
            order by r.wks_markersymbol'''
            ], 'auto')
        
        # Add descriptive table for data headings
        rosettaPage.append(
            '<TABLE BORDER=1 CELLPADDING=2 CELLSPACING=0 WIDTH="100%">'
                '<TR BGCOLOR="#D0E0F0" VALIGN=top ALIGN=left>'
                    '<TD ALIGN=CENTER WIDTH="40%">'
                        '<FONT COLOR="#000000" face="Arial,Helvetica">'
                        'Gene Symbols used in <BR><I>The Coat Colors of Mice '
                        '</I></FONT>'
                    '</TD>'
                    '<TD ALIGN=CENTER WIDTH="60%">'
                        '<FONT COLOR="#000000" face="Arial,Helvetica"> '
                        'Official Gene Nomenclature <BR>'
                        'from Mouse Genome Informatics</FONT>'
                    '</TD>'
                '</TR>'
            '</TABLE>')
        
        # Start data table and add column heading to the table
        rosettaPage.append ('<TABLE border=0 CELLPADDING=2 WIDTH="100%">'
            '<TR>'
                '<TD WIDTH="40%">Symbol in W.K. Silvers</TD>'
                '<TD WIDTH="30%">Current Gene Symbol</TD>'
                '<TD WIDTH="30%">Phenotypic Alleles</TD>'
            '</TR>'
            )
        
        # Add each row of query to the table
        for sqlRowNum in range(len(resultsList[0])):
            if self.totalRowCount%2 == 1:
                rowBGColor = '#FFFFFF'
            else:
                rowBGColor = '#DDDDDD'
                
            self.totalRowCount = self.totalRowCount + 1

            rosettaPage.append (tableRow % (
                rowBGColor,
                config['WKSBOOKURL'] + resultsList[0][sqlRowNum]['wks_markerurl'],
                mgi_html.doSubSupTags(str(resultsList[0][sqlRowNum]['wks_markersymbol'])),
                config['MGISEARCHES'] + 'accession_report.cgi?id=' + str(resultsList[0][sqlRowNum]['accid']),
                mgi_html.doSubSupTags(str(resultsList[0][sqlRowNum]['symbol'])),
                config['MGISEARCHES'] + 'allele_report.cgi?_Marker_key=' + str(resultsList[0][sqlRowNum]['_marker_key']),
                mgi_html.doSubSupTags(str(resultsList[0][sqlRowNum]['symbol'])) + ' allele(s)'
                ))

        # Close the data table
        rosettaPage.append ('</table>')

        return rosettaPage

    def main (self):
    #######################################################
    # Purpose: Driving routing of class.
    # Returns: Nothing
    # Assumes: Nothing
    # Effects: rosettaPage with is then returned to the user
    # Throws:  Nothing
    
        rosettaPage = self.openRosettaPage()
        
        rosettaPage = self.makeRosettaTable(rosettaPage)
        
        # Close the page
        rosettaPage.append ('<HR>')
        rosettaPage.append ('</BODY></HTML>')

        # output page to STDOUT
        for outputString in rosettaPage:
            print outputString
        
        return

################## 
### Main logic ###
##################
rosettaCGI = rosettaReportClass()

# the go() method from parent class simply wraps the main() in 
# error handling
rosettaCGI.go()