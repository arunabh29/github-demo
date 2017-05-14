
use strict;
use warnings;
use LWP::Simple;

sub main {

	$| = 1;

	my $input = 'C:\Users\TupuShumba\Perl_Workspace\Perl_Excercises\input.txt';
	my $output =
	  '>C:\Users\TupuShumba\Perl_Workspace\Perl_Excercises\output.txt';

	open( INPUT,  $input )  or die("Cannot open file: $input\n");
	open( OUTPUT, $output ) or die("Cannot open file: $output\n");

	while ( my $line = <INPUT> ) {

		if ( $line =~ /Ins/ ) {
			$line =~ s/Ins/Insurance Company/i;
			print( OUTPUT "$line" );
		}

	}

	close(OUTPUT);
	close(INPUT);
}

main();
