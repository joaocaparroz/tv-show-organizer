from pymkv import MKVFile, MKVTrack

input_folder = 'Y:\\Séries'
output_folder = 'Y:/Séries'
temp_folder = 'D:/temp'


mkv = MKVFile('D:/The Good Doctor S01E01 - Burnt Food.mkv')
if not [x for x in mkv.tracks if x.track_codec == 'SubRip/SRT' and x.language == 'por']:
    mkv.add_track('D:/The.Good.Doctor.S01E01.Burnt.Food.720p.AMZN.WEBRip.DDP5.1.x264-QOQ.srt')
    mkv.tracks[-1].language = 'por'
    mkv.mux('D:/The Good Doctor S01E01 - Burnt Food2.mkv')

if __name__ == '__main__':
    pass



