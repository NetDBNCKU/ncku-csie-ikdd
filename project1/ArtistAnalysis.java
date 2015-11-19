/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package edu.ncku.ikdd;

import java.io.IOException;
import java.util.Iterator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;

/**
 *
 * @author ril
 */
public class ArtistAnalysis {
    
    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {
        private static final Pattern pattern = Pattern.compile("^(\\d+)\\s+(\\d+)\\s+(\\d)\\s+(\\d)\\s+(\\d)\\s+(\\S.+)$");
        private Text summary = new Text(), artistName = new Text();
        
        public void map(LongWritable key, Text value, OutputCollector<Text, Text> output, Reporter reporter) {
            String line = value.toString();
            Matcher matcher = pattern.matcher(line);
            matcher.find();
            try {
                artistName.set(matcher.group(6));
                summary.set("1," + matcher.group(3) + "," + matcher.group(4) + "," + matcher.group(5));
                output.collect(artistName, summary);
            } catch (IllegalStateException ex) {
                ex.printStackTrace();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
    
    public static class Combine extends MapReduceBase implements Reducer<Text, Text, Text, Text> {
        private static final Pattern pattern = Pattern.compile("^(\\d+),(\\d+),(\\d+),(\\d+)$");
        private Text summary = new Text();
        
        public void reduce(Text key, Iterator<Text> values, OutputCollector<Text, Text> output, Reporter reporter) {
            int listen = 0, local = 0, skip = 0, fans = 0;
            String line;
            Matcher matcher;
            while (values.hasNext()) {
                line = values.next().toString();
                matcher = pattern.matcher(line);
                matcher.find();
                try {
                    fans += Integer.valueOf(matcher.group(1));
                    listen += Integer.valueOf(matcher.group(2));
                    local += Integer.valueOf(matcher.group(3));
                    skip += Integer.valueOf(matcher.group(4));
                } catch (IllegalStateException ex) {
                    System.err.println(line);
                    ex.printStackTrace();
                }
            }
            summary.set(String.valueOf(fans) + "," + String.valueOf(listen) + "," + String.valueOf(local) + "," + String.valueOf(skip));
            try {
                output.collect(key, summary);
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
    
    public static class Reduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {
        private static final Pattern pattern = Pattern.compile("^(\\d+),(\\d+),(\\d+),(\\d+)$");
        private Text summary = new Text();
        
        public void reduce(Text key, Iterator<Text> values, OutputCollector<Text, Text> output, Reporter reporter) {
            int listen = 0, local = 0, skip = 0, fans = 0;
            String line;
            Matcher matcher;
            while (values.hasNext()) {
                line = values.next().toString();
                matcher = pattern.matcher(line);
                matcher.find();
                try {
                    fans += Integer.valueOf(matcher.group(1));
                    listen += Integer.valueOf(matcher.group(2));
                    local += Integer.valueOf(matcher.group(3));
                    skip += Integer.valueOf(matcher.group(4));
                } catch (IllegalStateException ex) {
                    System.err.println(line);
                    ex.printStackTrace();
                }
            }
            summary.set(String.valueOf(fans) + "," + String.valueOf(listen) + "," + String.valueOf(local) + "," + String.valueOf(listen + local) + "," + String.valueOf(skip));
            try {
                output.collect(key, summary);
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
    
    public static void main(String[] argv) throws Exception {
        JobConf conf = new JobConf(ArtistAnalysis.class);
        conf.setJobName("artistanalysis");
        
        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Text.class);
        
        conf.setMapperClass(Map.class);
        conf.setCombinerClass(Combine.class);
        conf.setReducerClass(Reduce.class);
        
        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);
        
        FileInputFormat.setInputPaths(conf, new Path(argv[0]));
        FileOutputFormat.setOutputPath(conf, new Path(argv[1]));
        
        JobClient.runJob(conf);
    }
    
}
