#!/usr/bin/perl

use strict;
use warnings;

my $some_dir = ".";
opendir(DIR, $some_dir) || die "can't opendir $some_dir: $!";
my @files = grep { /yml/ } readdir(DIR);
closedir DIR;

foreach my $f (@files) {

    my $file = $f;
    #print "$file \n";
    
    open (FILE, '<', $file) or die "Could not open sample.txt: $!";
    
    my @in_lines = <FILE>;
    my $line;
    my $line1;
    
    foreach $line (@in_lines)  {
        if($line =~ /^object_translation_wrt_camera:/) {
    	  $line1 = $line;    
    #	  print "$line1";
    	}
    }
    
    my @chars = map substr( $line1, $_, 1), 0 .. length($line1) -1;
    my $char1 = '[';
    my $char2 = ',';
    my $index1 = index($line1, $char1);
    my $index2 = index($line1, $char2);
    my @char3;
    
    my $k = 0;
    for (my $i = $index1+1; $i < $index2; $i++) {
    	$char3[$k] = $chars[$i];
    	$k++;
    }
    
    my $first_num = $line1 =~ /(\f+)/;
    #print "$index1\n$index2\n";
    my $str = "@char3";
    (my $str_nospaces = $str) =~ s/\s//g;
    #print "$str_nospaces\n";
    
    my $filename = 'grt_report.txt';
    open(my $fh, '>>', $filename) or die "Could not open file '$filename' $!";
    print $fh "$file, $str_nospaces\n";
    close $fh;

}
