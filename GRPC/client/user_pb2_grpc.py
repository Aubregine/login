# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import user_pb2 as user__pb2


class UsersStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUsers = channel.unary_stream(
                '/Users/GetUsers',
                request_serializer=user__pb2.uEmpty.SerializeToString,
                response_deserializer=user__pb2.uUser.FromString,
                )
        self.GetUserByID = channel.unary_unary(
                '/Users/GetUserByID',
                request_serializer=user__pb2.uUserID.SerializeToString,
                response_deserializer=user__pb2.uUser.FromString,
                )
        self.AddUser = channel.unary_unary(
                '/Users/AddUser',
                request_serializer=user__pb2.uProtoUser.SerializeToString,
                response_deserializer=user__pb2.uResponse.FromString,
                )
        self.GetBookingForUser = channel.unary_unary(
                '/Users/GetBookingForUser',
                request_serializer=user__pb2.uUserID.SerializeToString,
                response_deserializer=user__pb2.uBooking.FromString,
                )
        self.GetMoviesForUser = channel.unary_stream(
                '/Users/GetMoviesForUser',
                request_serializer=user__pb2.uUserID.SerializeToString,
                response_deserializer=user__pb2.uMovie.FromString,
                )


class UsersServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserByID(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBookingForUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMoviesForUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UsersServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUsers': grpc.unary_stream_rpc_method_handler(
                    servicer.GetUsers,
                    request_deserializer=user__pb2.uEmpty.FromString,
                    response_serializer=user__pb2.uUser.SerializeToString,
            ),
            'GetUserByID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserByID,
                    request_deserializer=user__pb2.uUserID.FromString,
                    response_serializer=user__pb2.uUser.SerializeToString,
            ),
            'AddUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AddUser,
                    request_deserializer=user__pb2.uProtoUser.FromString,
                    response_serializer=user__pb2.uResponse.SerializeToString,
            ),
            'GetBookingForUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBookingForUser,
                    request_deserializer=user__pb2.uUserID.FromString,
                    response_serializer=user__pb2.uBooking.SerializeToString,
            ),
            'GetMoviesForUser': grpc.unary_stream_rpc_method_handler(
                    servicer.GetMoviesForUser,
                    request_deserializer=user__pb2.uUserID.FromString,
                    response_serializer=user__pb2.uMovie.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Users', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Users(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Users/GetUsers',
            user__pb2.uEmpty.SerializeToString,
            user__pb2.uUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUserByID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Users/GetUserByID',
            user__pb2.uUserID.SerializeToString,
            user__pb2.uUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Users/AddUser',
            user__pb2.uProtoUser.SerializeToString,
            user__pb2.uResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBookingForUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Users/GetBookingForUser',
            user__pb2.uUserID.SerializeToString,
            user__pb2.uBooking.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMoviesForUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Users/GetMoviesForUser',
            user__pb2.uUserID.SerializeToString,
            user__pb2.uMovie.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
