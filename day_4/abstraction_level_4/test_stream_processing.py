"""
Tests for the stream processing system.
"""
import unittest
from typing import Iterator, List

from stream_processing.core.base import StreamProcessor
from stream_processing.core.adapters import adapt_str_processor, str_processor_adapter
from stream_processing.processors.basic import (
    IdentityProcessor, 
    FilterProcessor, 
    TransformProcessor,
    SplitProcessor,
    JoinProcessor
)
from stream_processing.processors.stateful import (
    LineCountProcessor,
    DuplicateDetectorProcessor,
    AggregatorProcessor,
    BufferProcessor
)
from stream_processing.pipeline.builder import Pipeline


class StreamProcessingTests(unittest.TestCase):
    """Test cases for stream processing system."""
    
    def test_identity_processor(self):
        """Test that identity processor passes input unchanged."""
        processor = IdentityProcessor()
        input_stream = iter(["line1", "line2", "line3"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["line1", "line2", "line3"])
    
    def test_filter_processor(self):
        """Test that filter processor correctly filters inputs."""
        processor = FilterProcessor(min_length=5)
        input_stream = iter(["abc", "defgh", "ij", "klmno"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["defgh", "klmno"])
    
    def test_transform_processor(self):
        """Test that transform processor correctly transforms inputs."""
        processor = TransformProcessor(transform_func=lambda s: s.upper())
        input_stream = iter(["abc", "def", "ghi"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["ABC", "DEF", "GHI"])
    
    def test_split_processor(self):
        """Test that split processor correctly splits inputs."""
        processor = SplitProcessor(delimiter=",")
        input_stream = iter(["a,b,c", "d,e", "f"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["a", "b", "c", "d", "e", "f"])
    
    def test_join_processor(self):
        """Test that join processor correctly joins inputs."""
        processor = JoinProcessor(count=2, delimiter="-")
        input_stream = iter(["a", "b", "c", "d", "e"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["a-b", "c-d", "e"])
    
    def test_line_count_processor(self):
        """Test that line count processor correctly counts lines."""
        processor = LineCountProcessor(pattern="{count}: {line}")
        input_stream = iter(["a", "b", "c"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["1: a", "2: b", "3: c"])
    
    def test_duplicate_detector_processor(self):
        """Test that duplicate detector processor correctly handles duplicates."""
        processor = DuplicateDetectorProcessor(mode="skip")
        input_stream = iter(["a", "b", "a", "c", "b"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["a", "b", "c"])
    
    def test_adapter_for_str_processor(self):
        """Test that string processor adapter works correctly."""
        def reverse_string(s: str) -> str:
            return s[::-1]
        
        adapted_processor = str_processor_adapter(reverse_string)
        input_stream = iter(["abc", "def"])
        output_stream = adapted_processor(input_stream)
        self.assertEqual(list(output_stream), ["cba", "fed"])
    
    def test_pipeline(self):
        """Test that a pipeline works correctly with multiple processors."""
        pipeline = Pipeline([
            FilterProcessor(min_length=3),
            TransformProcessor(transform_func=lambda s: s.upper()),
            LineCountProcessor(pattern="Line {count}: {line}")
        ])
        
        input_stream = iter(["a", "abc", "de", "defg"])
        output_stream = pipeline.process(input_stream)
        self.assertEqual(list(output_stream), ["Line 1: ABC", "Line 2: DEFG"])
    
    def test_stateful_processor_reset(self):
        """Test that stateful processor can be reset."""
        processor = LineCountProcessor()
        
        # First run
        input_stream = iter(["a", "b"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["1: a", "2: b"])
        
        # Reset state
        processor.reset_state()
        
        # Second run
        input_stream = iter(["c", "d"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["1: c", "2: d"])
    
    def test_buffer_processor(self):
        """Test that buffer processor correctly buffers and processes lines."""
        processor = BufferProcessor(buffer_size=2, sort=True)
        input_stream = iter(["c", "a", "d", "b"])
        output_stream = processor.process(input_stream)
        self.assertEqual(list(output_stream), ["a", "c", "b", "d"])


if __name__ == "__main__":
    unittest.main()