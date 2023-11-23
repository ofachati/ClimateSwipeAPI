# Use an official Node.js runtime as a parent image
FROM node:18.18.0

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY Frontend/package*.json ./

# Install Angular dependencies
RUN npm install

# Copy the content of the local Frontend directory to the working directory
COPY Frontend/ .

# Expose port 4200
EXPOSE 4200

# Command to run the Angular application
CMD ["npm", "start"]
