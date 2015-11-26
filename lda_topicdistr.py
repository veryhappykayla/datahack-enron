# -*- coding: UTF-8 -*-
#!/usr/bin/env python

################################################################################

'''
LDA Topic Gatherer for Ungrams from Mallet Topic State file
Kayla Jacobs, based on sample code by Rafi Cohen

Assumes a topic model has been trained.
Outputs a file of unigrams with their topics and scores.

'''

################################################################################

debugMode = False
testMode = False

freqThreshold = 5       # Set to zero to effectively remove threshold
topicThreshold = 0      # Set to zero to effectively remove threshold

input_filename = r"lda\kam-topic-state"
output_unigram_filename = r"lda\kam-unigrams.txt"

################################################################################

print "lda_topicdistr"
print
print "Initializing..."
print

#-------------------------------------------------------------------------------    

# Open files


print "========================"
print "numTopics = " + str(numTopics)
print

input_file = open(input_filename, "rb")
output_unigram_file = open(output_unigram_filename, "wb")

# Print header for output:
header = "unigram" + "\t" + "count" + "\t" + "topics_list_with_scores" #+ "\t" + "num_topics_above_threshold"
print >> output_unigram_file, header

print "Input of MALLET topic state:"
print input_filename
print
print "Output of unigrams and their topics:"
print output_unigram_filename
print
print "Topic threshold = " + str(topicThreshold)
print "Frequency threshold = " + str(freqThreshold)
print

#-------------------------------------------------------------------------------    

print "Processing tokens in topic state..."

# Skip first three lines with other non-essential info
input_file.readline()
input_file.readline()
input_file.readline()

counts = defaultdict(lambda: defaultdict(int))

for line in input_file:
    data = line.rstrip().split()
    counts[data[-2]][data[-1]] +=1

#-------------------------------------------------------------------------------    

print "Consolidating topics..."

for word in counts:

    t_total = sum(counts[word].values())
    
    if t_total >= freqThreshold:
    
        w_t = defaultdict(float)
        for t in counts[word]:
            if float(counts[word][t])/t_total >= topicThreshold:
                w_t[t] = float(counts[word][t])/t_total
                
        ml = sorted([(value,int(item)) for item,value in w_t.iteritems()],reverse = True)
    
        toPrint =  word + "\t" + str(t_total) + "\t" + str(ml) # + "\t" + str(len(ml))
    
        if debugMode: print toPrint
        print >> output_unigram_file, toPrint

#-------------------------------------------------------------------------------    

input_file.close()
output_unigram_file.close()

#-------------------------------------------------------------------------------    

print "Finished! :)"