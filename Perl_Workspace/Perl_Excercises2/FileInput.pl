
use strict;
use warnings;
use LWP::Simple;

sub main {

	$| = 1;
	my $file = 'C:\Users\TupuShumba\Perl_Workspace\Perl_Excercises\monthly.txt';

	open( INPUT, $file ) or die("Cannot open file: $file\n");

	while ( my $line = <INPUT> ) {

		if ( $line =~ /Insurance/ ) {

			print("$line");
		}

	}

	close(INPUT);

}

main();
