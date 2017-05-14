# Demonstration of greedy and non-greedy quantifiers
use strict;
use warnings;
use LWP::Simple;

# * zero or more of preceding character, as many as possible.
# *? zero or more of preceding character, as few as possible.
# + one or more of preceding character, as many as possible.
# +? one or more of preceding character, as few as possible.
# {5} exactly five of the preceding.
# {3,6} atleast 3, at most 6 of the preceding.
# {3,} atleast 3, no limit on number of characters.
# $ has special meaning, so use \$ to match '$'.
 
sub main {

	$| = 1;
	my $text1 = 'DE$123456';
	my $text2 = 'DE789012$';
	
	if ( $text1 =~ /(DE\$\d{2,10})/i ) {

		print("Match: '$1'\n");
	}

	if ( $text2 =~ /(DE\d{2,}\$)/i ) {

		print("Match: '$1'\n");
	}

}

main();
