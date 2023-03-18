use Font::BDF::Reader;
use Data::Dumper;

my $BDF = Font::BDF::Reader->new('/home/pthomas/Desktop/sandbox/Untitled.bdf');
$BDF->read_bdf_metadata;
my $bdf_metadata = $BDF->get_bdf_metadata;
# From: http://www.cs.mcgill.ca/~abatko/computers/programming/perl/howto/hash/#print_the_keys_and_values_of_a_hash__given_a_hash_reference
while( my ($k, $v) = each %$bdf_metadata ) {
	print "$k $v\n";
}

my @startchars = $BDF->get_all_STARTCHAR;
foreach my $startchar (@startchars) {
	my $fontinfo = $BDF->get_font_info_by_STARTCHAR($startchar);
#	print Dumper($fontinfo), "\n";
#	my $dwidth = $fontinfo->{"DWIDTH"};
#	print "[$dwidth->[0],$dwidth->[1]]\n";
}
