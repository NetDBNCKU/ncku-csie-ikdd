/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package edu.ncku.ikdd;

import java.io.IOException;
import java.util.Iterator;
import java.util.regex.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;

/**
 *
 * @author ril
 */
public class TempRecord {
    
    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, IntWritable, IntWritable> {
        private static final Pattern pattern = Pattern.compile("\\d+99999(\\d{4}).+FM-12\\+.+9999999N0000001N9.0(\\d{3})1\\+99999.+");
        
        public void map(LongWritable key, Text value, OutputCollector<IntWritable, IntWritable> output, Reporter reporter) {
            String line = value.toString();
            Matcher matcher = pattern.matcher(line);
            matcher.find();
            try {
                output.collect(new IntWritable(Integer.valueOf(matcher.group(1))), new IntWritable(Integer.valueOf(matcher.group(2))));
            } catch (IllegalStateException ex) {
                ex.printStackTrace();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
    
    public static class Reduce extends MapReduceBase implements Reducer<IntWritable, IntWritable, IntWritable, IntWritable> {
        public void reduce(IntWritable key, Iterator<IntWritable> values, OutputCollector<IntWritable, IntWritable> output, Reporter reporter) {
            int tmp, max = -273;
            while (values.hasNext()) {
                tmp = values.next().get();
                if (tmp > max) {
                    max = tmp;
                }
            }
            try {
                output.collect(key, new IntWritable(max));
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
    
    public static void main(String[] argv) throws Exception {
        JobConf conf = new JobConf(TempRecord.class);
        conf.setJobName("temprecord");
        
        conf.setOutputKeyClass(IntWritable.class);
        conf.setOutputValueClass(IntWritable.class);
        
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