FROM nginx:alpine

# Copy the dashboard HTML to nginx's default serving directory
COPY dashboard.html /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
