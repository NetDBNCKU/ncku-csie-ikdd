/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package edu.ncku.ikdd;

import java.io.*;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.jsoup.Jsoup;

/**
 *
 * @author ril
 */
public class TitleParser {
    
    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {
        private static final String agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0";
        
        public void map(LongWritable key, Text value, OutputCollector<Text, Text> output, Reporter reporter) {
            String url = value.toString(), title = "";
            try {
                title = Jsoup.connect(url).userAgent(agent).timeout(20 * 1000).get().title();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            try {
                output.collect(value, new Text(title));
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
    
    public static class Reduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {
        public void reduce(Text key, Iterator<Text> values, OutputCollector<Text, Text> output, Reporter reporter) {
            while (values.hasNext()) {
                try {
                    output.collect(key, values.next());
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        }
    }
    
    public static void main(String[] argv) throws Exception {
        JobConf conf = new JobConf(TitleParser.class);
        conf.setJobName("titleparser");
        
        conf.setOutputKeyClass(Text.class);
        conf.setOutputValueClass(Text.class);
        
        conf.setMapperClass(Map.class);
        conf.setCombinerClass(Reduce.class);
        conf.setReducerClass(Reduce.class);
        
        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);
        
        FileInputFormat.setInputPaths(conf, new Path(argv[0]));
        FileOutputFormat.setOutputPath(conf, new Path(argv[1]));
        
        JobClient.runJob(conf);
    }
}