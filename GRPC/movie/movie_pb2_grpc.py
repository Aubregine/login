# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import movie_pb2 as movie__pb2


class MoviesStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetMovies = channel.unary_stream(
                '/Movies/GetMovies',
                request_serializer=movie__pb2.Empty.SerializeToString,
                response_deserializer=movie__pb2.Movie.FromString,
                )
        self.GetMovieByID = channel.unary_unary(
                '/Movies/GetMovieByID',
                request_serializer=movie__pb2.MovieID.SerializeToString,
                response_deserializer=movie__pb2.Movie.FromString,
                )
        self.GetMovieByTitle = channel.unary_unary(
                '/Movies/GetMovieByTitle',
                request_serializer=movie__pb2.MovieTitle.SerializeToString,
                response_deserializer=movie__pb2.Movie.FromString,
                )
        self.AddMovie = channel.unary_unary(
                '/Movies/AddMovie',
                request_serializer=movie__pb2.Movie.SerializeToString,
                response_deserializer=movie__pb2.Response.FromString,
                )
        self.DeleteMovie = channel.unary_unary(
                '/Movies/DeleteMovie',
                request_serializer=movie__pb2.MovieID.SerializeToString,
                response_deserializer=movie__pb2.Response.FromString,
                )


class MoviesServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetMovies(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMovieByID(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMovieByTitle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddMovie(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteMovie(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MoviesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetMovies': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMovies,
                    request_deserializer=movie__pb2.Empty.FromString,
                    response_serializer=movie__pb2.Movie.SerializeToString,
            ),
            'GetMovieByID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMovieByID,
                    request_deserializer=movie__pb2.MovieID.FromString,
                    response_serializer=movie__pb2.Movie.SerializeToString,
            ),
            'GetMovieByTitle': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMovieByTitle,
                    request_deserializer=movie__pb2.MovieTitle.FromString,
                    response_serializer=movie__pb2.Movie.SerializeToString,
            ),
            'AddMovie': grpc.unary_unary_rpc_method_handler(
                    servicer.AddMovie,
                    request_deserializer=movie__pb2.Movie.FromString,
                    response_serializer=movie__pb2.Response.SerializeToString,
            ),
            'DeleteMovie': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteMovie,
                    request_deserializer=movie__pb2.MovieID.FromString,
                    response_serializer=movie__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Movies', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Movies(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetMovies(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Movies/GetMovies',
            movie__pb2.Empty.SerializeToString,
            movie__pb2.Movie.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMovieByID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Movies/GetMovieByID',
            movie__pb2.MovieID.SerializeToString,
            movie__pb2.Movie.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMovieByTitle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Movies/GetMovieByTitle',
            movie__pb2.MovieTitle.SerializeToString,
            movie__pb2.Movie.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddMovie(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Movies/AddMovie',
            movie__pb2.Movie.SerializeToString,
            movie__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteMovie(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Movies/DeleteMovie',
            movie__pb2.MovieID.SerializeToString,
            movie__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
