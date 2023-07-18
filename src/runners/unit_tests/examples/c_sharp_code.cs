namespace Manufacturing.Shared.Core
{
    using System;

    public class Response
    {
        public bool Success { get; }

        public string Message { get; set; }

        public Exception Exception { get; set; }

        public Response(bool success)
        {
            Success = success;
        }

        public Response(bool success, string message)
        {
            Success = success;
            Message = message;
        }

        public static Response Failed(string message)
        {
            return Failed(message, null);
        }

        public static Response Failed(string message, Exception exception)
        {
            return new Response(false) { Message = message, Exception = exception };
        }

        public static Response Succeeded()
        {
            return new Response(true);
        }

        public static Response Succeeded(string message)
        {
            return new Response(true, message);
        }
    }

    public class Response<T> : Response
    {
        public T Value { get; private set; }

        private Response(bool success, T value)
            : base(success)
        {
            Value = value;
        }

        private Response(bool success, T value, string message) : base(success, message)
        {
            Value = value;
        }

        public new static Response<T> Failed(string message)
        {
            return Failed(message, null);
        }

        public new static Response<T> Failed(string message, Exception exception)
        {
            return new Response<T>(false, default(T)) { Message = message, Exception = exception };
        }

        public static Response<T> Succeeded(T value)
        {
            return new Response<T>(true, value);
        }

        public static Response<T> Succeeded(T value, string message)
        {
            return new Response<T>(true, value, message);
        }
    }
}