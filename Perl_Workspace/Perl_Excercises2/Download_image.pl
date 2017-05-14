
use strict;
use warnings;
use LWP::Simple;

sub main {

	print("Starting Google image download!\n");
	my $err_code = getstore('https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',"google_logo.png");

	if ( $err_code == 200 ) {

		print("Download successfully completed \n");
	}

	else {

		print("Download unsuccessful \n");
	}

	print("Done");

}

main();
