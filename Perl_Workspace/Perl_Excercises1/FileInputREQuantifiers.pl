# Demonstration of greedy and non-greedy quantifiers
use strict;
use warnings;
use LWP::Simple;

sub main {

	$| = 1;
	my $file = 'C:\Users\TupuShumba\Perl_Workspace\Perl_Excercises\comcast.txt';

	open( INPUT, $file ) or die("Cannot open file: $file\n");

	while ( my $line = <INPUT> ) {

		if ( $line =~ /(i.*?t)/i ) {

			print("Non-greedy match: '$1'\n");
		}

		if ( $line =~ /(i.*t)/i ) {

			print("Greedy match: '$1'\n");
		}

		print("***********************************************************************************************************************************\n");

	}

	close(INPUT);

}

main();
