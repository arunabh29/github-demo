
use strict;
use warnings;

$| = 1;

sub main {

	# \d digit
	# \s any space character
	# \S non-space
	# \w alphanumeric

	my $text1 = 'I am 117 years old tomorrow.';
	my $text2 = 'Iam117yearsoldtomorrow.';

	if ( $text1 =~ /(\d+)/ ) {
		print "Matched: '$1' \n";
	}

	if ( $text1 =~ /(am\s\d+)/ ) {

		print "Matched space: '$1' \n";
	}

	if ( $text2 =~ /(\w+)/ ) {

		print "Matched one or more alphanumeric: '$1' \n";
	}

	if ( $text2 =~ /(I\S+)/ ) {

		print "Matched zero or more non-space chars: '$1' \n";
	}

}

main();
