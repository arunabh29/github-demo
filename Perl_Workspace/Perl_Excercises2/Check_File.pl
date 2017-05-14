
use strict;
use warnings;
use LWP::Simple;

sub main {

	$|=1;
	my @files=('C:\Users\TupuShumba\Perl_Workspace\Perl_Excercises\google_logo.png', 'C:\Users\TupuShumba\Perl_Workspace\Perl_Excercises\.project', 'C:\Users\TupuShumba\Perl_Workspace\Perl_Excercises\Check_File.pl', 'C:\Users\TupuShumba\Perl_Workspace\Perl_Excercises\Hello.pl', 'C:\Users\TupuShumba\Perl_Workspace\Perl_Excercises\Missing.txt',);
	


	foreach my $file(@files){
		
		if ( -f $file ) {

		print("File found: $file\n");
	}
	else {

		print("File does not exist: $file\n");
	}
		
		
	}
	  

}

main();
