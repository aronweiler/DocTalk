namespace Manufacturing.Shared.Core
{
    using System;

    public class Response
    {
        public bool Success { get; }

        public string Message { get; protected set; }

        public Exception Exception { get; protected set; }

        protected Response(bool success)
        {
            Success = success;
        }

        protected Response(bool success, string message)
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
}