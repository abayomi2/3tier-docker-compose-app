# Use a Node.js image for the backend API
FROM node:16

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install cors

# Copy the source code
COPY . .

# Expose port 5000 for the API
EXPOSE 5000

# Start the backend server
CMD ["node", "app.js"]
