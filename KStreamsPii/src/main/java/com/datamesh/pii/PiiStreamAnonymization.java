package com.datamesh.pii;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.TopologyDescription;
import org.apache.kafka.streams.kstream.KStream;

import org.apache.kafka.streams.kstream.internals.InternalStreamsBuilder;
import org.apache.kafka.streams.kstream.internals.KStreamImpl;
import org.apache.kafka.streams.processor.internals.InternalTopologyBuilder;
import org.json.JSONObject;
import org.springframework.util.ReflectionUtils;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.IOException;

import java.lang.reflect.Field;
import java.net.HttpURLConnection;
import java.net.URL;

import java.util.Properties;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;

public final class PiiStreamAnonymization {
    private static final String inputTopic = "random-pii-text";
    private static final String outputTopic = "random-pii-text-anon";
    private static final String restServiceUri = "http://localhost:10995/v1/singleAnonymizePII";

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

        try {

            //
            // random APPLICATION_ID_CONFIG allows stream to reprocess from the beginning. This is typically
            // not desirable, but was useful for this demo.
            String applicationId = UUID.randomUUID().toString();
            props.putIfAbsent(StreamsConfig.APPLICATION_ID_CONFIG, applicationId);
            props.putIfAbsent(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:19092,localhost:29092,localhost:39092");
            props.putIfAbsent(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
            props.putIfAbsent(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());

            props.putIfAbsent(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
            props.putIfAbsent(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
            props.putIfAbsent(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
            props.putIfAbsent(ConsumerConfig.GROUP_ID_CONFIG, UUID.randomUUID().toString());

        } catch(Exception e) {
            System.err.println("Error: " + e.getMessage());
        }

        return props;
    }

    private static void createAnonymizedPiiStream(final StreamsBuilder builder) {
        final KStream<String, String> source = builder.stream(inputTopic);

        try {
            source.mapValues(message -> anonymizePiiFromApi(new JSONObject(message))).to(outputTopic);
        } catch(Exception e) {
            System.err.println(e.getMessage());
        }
    }

    private static String anonymizePiiFromApi(JSONObject rawInput) {

        StringBuilder sb = new StringBuilder();

        try {
            URL url = new URL(restServiceUri);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();

            conn.setDoOutput(true);
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setRequestMethod("PUT");

            OutputStreamWriter out = new OutputStreamWriter(conn.getOutputStream());
            out.write(rawInput.toString());
            out.close();

            if(conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
                InputStreamReader streamReader = new InputStreamReader(conn.getInputStream());
                BufferedReader bufferedReader = new BufferedReader(streamReader);
                String response;
                while ((response = bufferedReader.readLine()) != null) {
                    sb.append(response).append("\n");
                }
                bufferedReader.close();
            }

        } catch(Exception e) {
            System.err.println("Error: " + e.getMessage());
        }

        return sb.toString();
    }

    public static void main(final String[] args) throws IOException, IllegalAccessException {
        final Properties props = getStreamsConfig(args);
        final StreamsBuilder builder = new StreamsBuilder();

        createAnonymizedPiiStream(builder);

        final KafkaStreams streams = new KafkaStreams(builder.build(), props);
        final CountDownLatch latch = new CountDownLatch(1);

        System.out.println(builder.build().describe());

        // attach shutdown handler to catch control-c
        Runtime.getRuntime().addShutdownHook(new Thread("pii-anon-shutdown-hook") {
            @Override
            public void run() {
                streams.close();
                latch.countDown();
            }
        });

        try {
            streams.start();
            latch.await();
        } catch (final Throwable e) {
            System.exit(1);
        }

        System.exit(0);
    }
}
