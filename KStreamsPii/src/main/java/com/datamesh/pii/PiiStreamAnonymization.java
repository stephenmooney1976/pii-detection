package com.datamesh.pii;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.IOException;

import java.net.HttpURLConnection;
import java.net.URL;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import java.util.Properties;

public final class PiiStreamAnonymization {
    private static final String inputTopic = "random-pii-text";
    private static final String outputTopic = "random-pii-text-anon";
    private static final String restServiceUri = "http://localhost:10995/v1/singleAnonymizePII";


    //private Properties streamsConfiguration = new Properties();

    static Properties getStreamsConfig(final String[] args) throws IOException {
        final Properties props = new Properties();
        if(args != null && args.length > 0) {
            try (final FileInputStream fis = new FileInputStream(args[0])) {
                props.load(fis);
            }
            if(args.length > 1) {
                System.out.println("Warning: Some command line arguments were ignored.");
            }
        }

        props.putIfAbsent(StreamsConfig.APPLICATION_ID_CONFIG, "streams-pii-anon");
        props.putIfAbsent(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.putIfAbsent(StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG, 0);
        props.putIfAbsent(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        props.putIfAbsent(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());

        props.putIfAbsent(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        return props;
    }

    static void createAnonymizedPiiStream(final StreamsBuilder builder) {
        final KStream<String, String> source = builder.stream(inputTopic);
        
    }

    public static void main(final String[] args) throws IOException {
      final Properties props = getStreamsConfig(args);

      try {

          URL url = new URL("http://localhost:10995/v1/singleAnonymizePII");
          HttpURLConnection conn = (HttpURLConnection) url.openConnection();

          JSONObject piiObject = new JSONObject();
          piiObject.put("recordId", "AAAA1234");
          piiObject.put("inputText", "My phone number is 312.434.2415");

          conn.setDoOutput(true);
          conn.setRequestProperty("Content-Type", "application/json");
          conn.setRequestMethod("PUT");

          OutputStreamWriter out = new OutputStreamWriter(conn.getOutputStream());
          out.write(piiObject.toString());
          out.close();

          StringBuilder stringBuilder = new StringBuilder();

          if(conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
              InputStreamReader streamReader = new InputStreamReader(conn.getInputStream());
              BufferedReader bufferedReader = new BufferedReader(streamReader);
              String response = null;
              while ((response = bufferedReader.readLine()) != null) {
                  stringBuilder.append(response + "\n");
              }
              bufferedReader.close();
          }

          System.out.println(stringBuilder.toString());

          //String resp = conn.getResponseMessage();
          //#System.out.println(resp);

      } catch(Exception e) {
          System.err.println("Error: " + e.getMessage());
      }
    }


}
