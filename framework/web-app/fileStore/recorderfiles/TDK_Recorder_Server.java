/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.InetAddress;
import java.io.BufferedReader;
import java.io.FileReader;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.InputStream;
import java.net.NetworkInterface;
import java.util.Enumeration;
import java.net.Inet4Address;
import java.util.Timer;
import java.util.TimerTask;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;

public class TDK_Recorder_Server extends TimerTask {
    public void run() {
	//WriteFile("No message  Received on Status Server");
	System.out.println("No message  Received on Status Server");
       	System.exit(0);
    }
 



	static	String long_poll_data = "code=0\n"+"data="+
		"{url=http://{ip}:8001/updateSchedule;response=http://{ip}:8002/status;updatetime={currentTime}}";
	static String schedule ="";
	public static void main(String[] args) throws Exception
	{   

		Timer timer = new Timer();
		timer.schedule(new TDK_Recorder_Server(), 360*1000);


		if(args.length == 1)
		{
			if(args[0].equals("-h"))
			{
				Help();
				System.exit(0);
			}
			else
			{
				schedule = args[0];
			}
		}
		else
		{
			//System.out.println("Invalid No. of Agruments\n");
			Help();
			System.exit(0);
		}
		long currentTime = System.currentTimeMillis();
		NetworkInterface ni = NetworkInterface.getByName("eth0");
		Enumeration inetEnum =ni.getInetAddresses();
		while(inetEnum.hasMoreElements())
		{
			InetAddress inet = (InetAddress)inetEnum.nextElement();
			if (inet instanceof Inet4Address)
			{
		//		System.out.println("IP addr is : " +inet.getHostAddress());
				long_poll_data=long_poll_data.replaceAll("\\{ip\\}",inet.getHostAddress());

				break;
			}
			else  
				continue;
		}
		if((schedule = readFile(schedule)) == null)
		{
			System.out.println("Not able to read "+schedule);	     
			System.exit(0);
		}


		//System.out.println("schedule="+schedule);
		long_poll_data =long_poll_data.replaceAll("\\{currentTime\\}", ""+currentTime);
		//System.out.println("long_poll_data"+long_poll_data);
		HttpServer lpServer = HttpServer.create(new InetSocketAddress(8000), 0);
		lpServer.createContext("/longpollServer", new LPSHandler());
		lpServer.setExecutor(null); 
		lpServer.start();

		HttpServer rwsServer = HttpServer.create(new InetSocketAddress(8001), 1);
		rwsServer.createContext("/updateSchedule", new RWSHandler());
		rwsServer.setExecutor(null); 
		rwsServer.start();

		HttpServer rwspServer = HttpServer.create(new InetSocketAddress(8002), 2);
		rwspServer.createContext("/status", new RWSStatusHandler());
		rwspServer.setExecutor(null); 
		rwspServer.start();

	}

	private static void  Help()
	{
		System.out.println("Usage: java TDK_Recorder_Server <filename>]\n"
				+ "<filename>                  filename with schedule json command\n"
				+ "-h                          print help message\n"
				+ "\n"
				+ "Example:\n"
				+ " java TDK_Recorder_Server schedule.json \n");
	}


	static class LPSHandler implements HttpHandler
	{
		public void handle(HttpExchange t) throws IOException 
		{
			String response =long_poll_data;
			t.sendResponseHeaders(200, response.length());
			OutputStream os = t.getResponseBody();
			os.write(response.getBytes());
			os.close();
		}
	}

	static class RWSHandler implements HttpHandler
	{
		public void handle(HttpExchange t) throws IOException 
		{
			String response =schedule;
			t.sendResponseHeaders(200, response.length());
			OutputStream os = t.getResponseBody();
			os.write(response.getBytes());
			os.close();
		}
	}

	static class RWSStatusHandler implements HttpHandler
	{
		public void handle(HttpExchange t) throws IOException 
		{
			InputStream in = t.getRequestBody();
			int noOfBytes = in.available();
			byte[]b= new byte[noOfBytes];
			in.read(b);
			in.close();
			System.out.println( new String(b));
			//WriteFile(new String(b));
			System.exit(0);
		}
	}


	public static String readFile(String commandName)
	{
		String command =null;
		BufferedReader br = null;
		try
		{

			String sCurrentLine;

			br = new BufferedReader(new FileReader(commandName));

			StringBuffer buffer = new StringBuffer("");
			while ((sCurrentLine = br.readLine()) != null) 
			{
				buffer.append(sCurrentLine);
			}
			command = buffer.toString();
		} 
		catch (IOException e) 
		{
			e.printStackTrace();
		}
		finally
		{
			try {
				if (br != null)
					br.close();
			}
			catch (IOException ex) 
			{
				ex.printStackTrace();
			}
		}
		return command;
	}
/* 
	public static void WriteFile(String Status) {
		try {
 
 
			File file = new File("Status.txt");
 
			// if file doesnt exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}
 
			FileWriter fw = new FileWriter(file.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);
			bw.write(Status);
			bw.close();
 
			//System.out.println("Done");
 
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
*/
}


