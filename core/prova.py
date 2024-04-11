import srx_segmenter
import os

srx_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'linguistic-data/segment.srx')
rules = srx_segmenter.parse(srx_filepath)



text =  "Sense pensar-ho. Tot per tu. Fins demà. Fins avui."
segmenter = srx_segmenter.SrxSegmenter(rules["Catalan"], text)
segments, whitespaces = segmenter.extract()
print("segments:" + str(segments))
print("segments:" + str(len(segments)))
